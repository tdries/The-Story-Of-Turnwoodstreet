-- ── Fix 1 (CRITICAL): Lock down players table SELECT ─────────────────────────
-- Problem: anon key can read ALL player PII (emails, names, user_ids).
-- Solution: restrict SELECT to own row only, add a public scoreboard view.

-- Drop any permissive SELECT policy (try common names)
DROP POLICY IF EXISTS "public read" ON players;
DROP POLICY IF EXISTS "anyone can read" ON players;
DROP POLICY IF EXISTS "anon read" ON players;
DROP POLICY IF EXISTS "select" ON players;
DROP POLICY IF EXISTS "Enable read access for all users" ON players;

-- Players can only read their own row
DROP POLICY IF EXISTS "read own player" ON players;
CREATE POLICY "read own player"
  ON players FOR SELECT
  USING (auth.uid() = user_id);

-- Public scoreboard view (no email, no user_id, no email_optin)
CREATE OR REPLACE VIEW public_scoreboard AS
  SELECT
    p.display_name,
    p.avatar_url,
    p.playtime_seconds,
    p.items_collected,
    p.feedback_count,
    COALESCE((SELECT count(*) FROM guestbook g WHERE g.user_id = p.user_id), 0)::int AS guestbook_count
  FROM players p
  ORDER BY p.playtime_seconds DESC
  LIMIT 50;

-- Grant anon + authenticated access to the view
GRANT SELECT ON public_scoreboard TO anon, authenticated;


-- ── Fix 5 (HIGH): Guestbook INSERT must check user_id ownership ──────────────
-- Problem: any authenticated user can insert with any user_id.

DROP POLICY IF EXISTS "auth insert" ON guestbook;
DROP POLICY IF EXISTS "auth insert own" ON guestbook;
CREATE POLICY "auth insert own"
  ON guestbook FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = user_id);


-- ── Fix 8 (MEDIUM): feedback_submissions needs a SELECT policy ───────────────
-- Problem: no SELECT policy means scoreboard feedback_count is always 0.
-- Solution: allow authenticated users to read their own submissions.

DROP POLICY IF EXISTS "read own feedback" ON feedback_submissions;
CREATE POLICY "read own feedback"
  ON feedback_submissions FOR SELECT TO authenticated
  USING (auth.uid() = user_id);
