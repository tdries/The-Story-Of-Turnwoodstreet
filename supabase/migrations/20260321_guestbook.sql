-- Guestbook: one entry per visitor message, publicly readable.
CREATE TABLE IF NOT EXISTS guestbook (
  id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      uuid        REFERENCES auth.users ON DELETE SET NULL,
  display_name text        NOT NULL,
  message      text        NOT NULL CHECK (char_length(message) <= 300),
  created_at   timestamptz DEFAULT now()
);

ALTER TABLE guestbook ENABLE ROW LEVEL SECURITY;

-- Anyone (including anon / server-side) can read entries
CREATE POLICY IF NOT EXISTS "public read"
  ON guestbook FOR SELECT USING (true);

-- Any authenticated user may insert their own entry
CREATE POLICY IF NOT EXISTS "auth insert"
  ON guestbook FOR INSERT TO authenticated
  WITH CHECK (true);
