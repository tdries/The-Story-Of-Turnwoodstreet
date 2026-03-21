/**
 * server.js — Express server for Turnhoutsebaan RPG
 * Serves the Vite build + provides /api/news (scraped from hln.be/borgerhout, cached 4h)
 */

'use strict';

const express  = require('express');
const https    = require('https');
const http     = require('http');
const path     = require('path');
const cheerio  = require('cheerio');

const app  = express();
const PORT = process.env.PORT || 3000;

const NEWS_URL = 'https://www.hln.be/borgerhout/';
const CACHE_TTL = 4 * 60 * 60 * 1000; // 4 hours

let cache = { headlines: [], fetchedAt: 0 };

// ── HTTP GET helper ──────────────────────────────────────────────────────────
function get(url, redirects = 5) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const req = lib.get(url, {
      headers: {
        'User-Agent':      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'nl-BE,nl;q=0.9,fr;q=0.7,en;q=0.5',
        'Accept-Encoding': 'identity',
        'Cache-Control':   'no-cache',
      },
    }, (res) => {
      // Follow redirects
      if ((res.statusCode === 301 || res.statusCode === 302) && res.headers.location && redirects > 0) {
        return get(res.headers.location, redirects - 1).then(resolve).catch(reject);
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
      '.article__title',
      '.teaser__title',
      '.js-article-title',
      '[data-article-title]',
      'h3[class*="title"]',
      'h2[class*="title"]',
      '.card__title',
      '.item__title',
    ];
    for (const sel of selectors) {
      $(sel).each((_, el) => add($(el).text()));
    }

    if (headlines.length === 0) {
      // Last resort: all <a> tags inside <article> that look like headlines
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
      console.warn('[news] no headlines found in page — keeping stale cache');
    }
    return cache.headlines;

  } catch (err) {
    console.error('[news] scrape error:', err.message);
    return cache.headlines; // stale cache on error
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

// ── Routes ───────────────────────────────────────────────────────────────────
app.use(express.static(path.join(__dirname, 'dist'), {
  setHeaders(res) {
    res.set('X-Frame-Options',        'SAMEORIGIN');
    res.set('X-Content-Type-Options', 'nosniff');
    res.set('Referrer-Policy',        'no-referrer');
  },
}));

app.get('/api/news', async (req, res) => {
  const headlines = await getNews();
  res.json({ headlines, fetchedAt: cache.fetchedAt });
});

// SPA fallback
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(PORT, () => console.log(`[server] listening on :${PORT}`));
