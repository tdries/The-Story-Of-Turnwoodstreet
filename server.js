/**
 * server.js — Express server for Turnhoutsebaan RPG
 * Serves the Vite build + provides:
 *   GET  /api/news           — scraped hln.be/borgerhout headlines, cached 4h
 *   POST /api/github-webhook — receives GitHub issue events, sends thank-you e-mails
 */

'use strict';

const express  = require('express');
const https    = require('https');
const http     = require('http');
const path     = require('path');
const cheerio  = require('cheerio');
const crypto   = require('crypto');

const app  = express();
const PORT = process.env.PORT || 3000;

const NEWS_URL  = 'https://www.hln.be/borgerhout/';
const CACHE_TTL = 4 * 60 * 60 * 1000; // 4 hours

// Fallback when hln.be is unavailable
const FALLBACK_NEWS = [
  'Turnhoutsebaan wint prijs voor meest levendige winkelstraat van Borgerhout',
  'Nieuwe fietsinfrastructuur op de Turnhoutsebaan: meer ruimte voor fietsers',
  'Borger Hub verwelkomt nieuw kunstenaarscollectief in wijk',
  'Frituur De Tram viert 30ste verjaardag met gratis friet voor buurtbewoners',
  'Theehuys Amal organiseert open deur voor buurtbewoners',
  'Hammam Borgerhout breidt uit met nieuw wellness-aanbod',
  'Budget Market verlaagt prijzen voor lokale klanten',
  'Patisserie Aladdin wint gouden ster voor beste baklava van Antwerpen',
];

let cache = { headlines: [], fetchedAt: 0 };

// ── HTTP helpers ──────────────────────────────────────────────────────────────

function get(url, redirects = 5, extraHeaders = {}) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const req = lib.get(url, {
      headers: {
        'User-Agent':      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'nl-BE,nl;q=0.9,fr;q=0.7,en;q=0.5',
        'Accept-Encoding': 'identity',
        'Cache-Control':   'no-cache',
        ...extraHeaders,
      },
    }, (res) => {
      if ((res.statusCode === 301 || res.statusCode === 302) && res.headers.location && redirects > 0) {
        return get(res.headers.location, redirects - 1, extraHeaders).then(resolve).catch(reject);
      }
      let data = '';
      res.setEncoding('utf8');
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    });
    req.setTimeout(12000, () => { req.destroy(); reject(new Error('timeout')); });
    req.on('error', reject);
  });
}

function post(url, jsonBody, extraHeaders = {}) {
  return new Promise((resolve, reject) => {
    const payload = Buffer.from(JSON.stringify(jsonBody));
    const opts = new URL(url);
    const req = https.request({
      hostname: opts.hostname,
      path:     opts.pathname + opts.search,
      method:   'POST',
      headers: {
        'Content-Type':   'application/json',
        'Content-Length': payload.length,
        ...extraHeaders,
      },
    }, (res) => {
      let data = '';
      res.setEncoding('utf8');
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => resolve({ status: res.statusCode, body: data }));
    });
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('timeout')); });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ── Supabase REST helpers ─────────────────────────────────────────────────────

function supabaseHeaders(key) {
  return { 'apikey': key, 'Authorization': `Bearer ${key}` };
}

async function supabaseGet(path) {
  const supaUrl = process.env.VITE_SUPABASE_URL;
  const svcKey  = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!supaUrl || !svcKey) return [];
  try {
    const { status, body } = await get(`${supaUrl}/rest/v1/${path}`, 5, supabaseHeaders(svcKey));
    if (status !== 200) { console.warn('[supabase] GET error', status); return []; }
    return JSON.parse(body);
  } catch (e) {
    console.error('[supabase] request error:', e.message);
    return [];
  }
}

// ── Scraper ──────────────────────────────────────────────────────────────────

async function scrapeNews() {
  console.log('[news] fetching', NEWS_URL);
  try {
    const { status, body } = await get(NEWS_URL);
    if (status !== 200) throw new Error(`HTTP ${status}`);

    const $ = cheerio.load(body);
    const headlines = [];
    const seen = new Set();

    function add(text) {
      const t = text.replace(/\s+/g, ' ').trim();
      if (t.length > 15 && t.length < 220 && !seen.has(t)) {
        seen.add(t);
        headlines.push(t);
      }
    }

    // 1. JSON-LD structured data (most reliable when present)
    $('script[type="application/ld+json"]').each((_, el) => {
      try {
        const data = JSON.parse($(el).html() || '{}');
        const nodes = Array.isArray(data) ? data : [data];
        for (const node of nodes) {
          if (node.headline) add(node.headline);
          if (node.name && node['@type'] === 'NewsArticle') add(node.name);
          if (Array.isArray(node.itemListElement)) {
            node.itemListElement.forEach(li => {
              if (li?.item?.name) add(li.item.name);
              if (li?.name)       add(li.name);
            });
          }
        }
      } catch (_) {}
    });

    // 2. HTML selector fallbacks (DPG Media / hln.be patterns)
    const selectors = [
      'article h3', 'article h2', 'article h1',
      '.article__title', '.teaser__title', '.js-article-title',
      '[data-article-title]', 'h3[class*="title"]', 'h2[class*="title"]',
      '.card__title', '.item__title',
    ];
    for (const sel of selectors) {
      $(sel).each((_, el) => add($(el).text()));
    }

    if (headlines.length === 0) {
      $('article a').each((_, el) => {
        const t = $(el).text().trim();
        if (t.length > 25 && t.length < 200 && !/^(meer|lees|bekijk)/i.test(t)) add(t);
      });
    }

    const result = headlines.slice(0, 20);
    if (result.length > 0) {
      cache = { headlines: result, fetchedAt: Date.now() };
      console.log(`[news] cached ${result.length} headlines`);
    } else {
      console.warn('[news] no headlines found — using fallback');
      cache = { headlines: FALLBACK_NEWS, fetchedAt: Date.now() };
    }
    return cache.headlines;

  } catch (err) {
    console.error('[news] scrape error:', err.message);
    if (cache.headlines.length === 0) cache = { headlines: FALLBACK_NEWS, fetchedAt: Date.now() };
    return cache.headlines;
  }
}

// ── Guestbook (Supabase REST) ────────────────────────────────────────────────

async function fetchGuestbookEntries() {
  const supaUrl = process.env.VITE_SUPABASE_URL;
  const supaKey = process.env.VITE_SUPABASE_ANON_KEY;
  if (!supaUrl || !supaKey) return [];
  try {
    const apiUrl = `${supaUrl}/rest/v1/guestbook?select=display_name,message&order=created_at.desc&limit=8`;
    const { status, body } = await get(apiUrl, 5, supabaseHeaders(supaKey));
    if (status !== 200) return [];
    const rows = JSON.parse(body);
    return rows.map(r => `✍ ${r.display_name || 'Anoniem'}: ${r.message}`).filter(s => s.length < 180);
  } catch (e) {
    console.warn('[guestbook] fetch error:', e.message);
    return [];
  }
}

async function getNews() {
  if (Date.now() - cache.fetchedAt < CACHE_TTL && cache.headlines.length > 0) {
    return cache.headlines;
  }
  return scrapeNews();
}

// Warm cache on startup, then refresh every 4h
getNews();
setInterval(scrapeNews, CACHE_TTL);

// ── Feedback-resolved e-mail ──────────────────────────────────────────────────

async function getSubmissionsForIssue(issueNumber) {
  return supabaseGet(
    `feedback_submissions?github_issue_number=eq.${issueNumber}&select=email,category,message`,
  );
}

async function sendThankYouEmail(email, issueNumber, category, message) {
  const apiKey = process.env.RESEND_API_KEY;
  const from   = process.env.RESEND_FROM || 'Turnwoodstreet <noreply@premiumbrick.com>';
  if (!apiKey) {
    console.warn('[email] RESEND_API_KEY not set — skipping mail to', email);
    return false;
  }

  const preview  = message ? message.slice(0, 80).replace(/\n/g, ' ') : '';
  const catLabel = category || 'feedback';

  const html = `
<!DOCTYPE html>
<html lang="nl">
<head><meta charset="utf-8"></head>
<body style="background:#0A0A12;color:#F0EAD6;font-family:sans-serif;padding:32px;max-width:540px;margin:0 auto;">
  <h1 style="color:#FFD700;font-size:22px;margin-bottom:4px;">🎮 We hebben naar je geluisterd!</h1>
  <p style="color:#aaa;margin-top:0;font-size:13px;">Issue #${issueNumber} is opgelost.</p>
  <hr style="border:none;border-top:1px solid #333;margin:20px 0;">
  <p style="font-size:15px;line-height:1.6;">
    Jouw <strong style="color:#FFD700;">${catLabel}</strong>-feedback is verwerkt in het spel:
  </p>
  <blockquote style="border-left:3px solid #FFD700;margin:16px 0;padding:8px 16px;color:#ccc;font-style:italic;">
    "${preview}${message && message.length > 80 ? '…' : ''}"
  </blockquote>
  <p style="font-size:15px;line-height:1.6;">
    Bedankt dat je <strong style="color:#FFD700;">Turnwoodstreet</strong> het spel van de eeuw helpt maken. 🏆
  </p>
  <hr style="border:none;border-top:1px solid #333;margin:20px 0;">
  <p style="font-size:12px;color:#666;">
    Dit is een automatisch bericht van het Turnwoodstreet-team.<br>
    Speel mee op <a href="https://turnwoodstreet.be" style="color:#FFD700;">turnwoodstreet.be</a>
  </p>
</body>
</html>`;

  try {
    const { status, body } = await post(
      'https://api.resend.com/emails',
      { from, to: [email], subject: 'We hebben naar je geluisterd! 🎮 Turnwoodstreet', html },
      { 'Authorization': `Bearer ${apiKey}` },
    );
    if (status >= 200 && status < 300) {
      console.log(`[email] sent to ${email} for issue #${issueNumber}`);
      return true;
    }
    console.warn(`[email] Resend error ${status}: ${body}`);
    return false;
  } catch (e) {
    console.error('[email] send error:', e.message);
    return false;
  }
}

// ── Routes ───────────────────────────────────────────────────────────────────

app.use(express.static(path.join(__dirname, 'dist'), {
  setHeaders(res) {
    res.set('X-Frame-Options',        'SAMEORIGIN');
    res.set('X-Content-Type-Options', 'nosniff');
    res.set('Referrer-Policy',        'no-referrer');
  },
}));

app.get('/api/news', async (req, res) => {
  const [headlines, guestbook] = await Promise.all([getNews(), fetchGuestbookEntries()]);
  res.json({ headlines: [...headlines, ...guestbook], fetchedAt: cache.fetchedAt });
});

// GitHub webhook — must use express.raw to preserve body for HMAC verification
app.post('/api/github-webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  // ── 1. Verify signature ───────────────────────────────────────────────────
  const secret = process.env.GITHUB_WEBHOOK_SECRET;
  const sig    = req.headers['x-hub-signature-256'];
  if (secret) {
    if (!sig) return res.status(401).send('Missing signature');
    const expected = 'sha256=' + crypto.createHmac('sha256', secret).update(req.body).digest('hex');
    try {
      if (!crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(sig))) {
        return res.status(401).send('Bad signature');
      }
    } catch {
      return res.status(401).send('Bad signature');
    }
  }

  // ── 2. Parse & filter ─────────────────────────────────────────────────────
  const event   = req.headers['x-github-event'];
  const payload = JSON.parse(req.body.toString());

  if (event !== 'issues' || payload.action !== 'closed') {
    return res.json({ ok: true, skipped: true });
  }

  const issueNumber = payload.issue.number;
  console.log(`[webhook] issue #${issueNumber} closed`);

  // ── 3. Look up submitters ─────────────────────────────────────────────────
  const submissions = await getSubmissionsForIssue(issueNumber);
  const uniqueEmails = [...new Set(submissions.map(s => s.email).filter(Boolean))];

  if (uniqueEmails.length === 0) {
    console.log(`[webhook] no e-mail submissions for issue #${issueNumber}`);
    return res.json({ ok: true, emails_sent: 0 });
  }

  // ── 4. Send thank-you mails ───────────────────────────────────────────────
  let sent = 0;
  for (const email of uniqueEmails) {
    const sub = submissions.find(s => s.email === email);
    if (await sendThankYouEmail(email, issueNumber, sub?.category, sub?.message)) sent++;
  }

  console.log(`[webhook] sent ${sent}/${uniqueEmails.length} thank-you mails for issue #${issueNumber}`);
  res.json({ ok: true, emails_sent: sent });
});

// SPA fallback — use app.use so it works in Express 4 and 5
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(PORT, () => console.log(`[server] listening on :${PORT}`));
