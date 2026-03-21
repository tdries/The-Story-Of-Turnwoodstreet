-- Track which player submitted which GitHub issue, so we can e-mail them
-- when their feedback item is resolved.
CREATE TABLE IF NOT EXISTS feedback_submissions (
  id                  uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id             uuid        REFERENCES auth.users ON DELETE SET NULL,
  email               text,
  github_issue_number integer     NOT NULL,
  category            text,
  message             text,
  created_at          timestamptz DEFAULT now()
);

ALTER TABLE feedback_submissions ENABLE ROW LEVEL SECURITY;

-- Players may insert only their own rows (or anonymous rows when not logged in)
CREATE POLICY "insert own feedback"
  ON feedback_submissions FOR INSERT
  WITH CHECK (auth.uid() = user_id OR user_id IS NULL);
