-- One save slot per player — upserted on every explicit save.
-- The state column holds the full GameState JSON blob.
CREATE TABLE IF NOT EXISTS save_states (
  user_id  uuid        PRIMARY KEY REFERENCES auth.users ON DELETE CASCADE,
  state    jsonb       NOT NULL,
  saved_at timestamptz DEFAULT now()
);

ALTER TABLE save_states ENABLE ROW LEVEL SECURITY;

-- Each player can only read and write their own save
CREATE POLICY "own save"
  ON save_states FOR ALL
  USING      (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
