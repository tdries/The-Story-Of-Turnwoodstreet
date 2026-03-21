-- Migration: add email_optin flag to players table
-- NULL  = not yet asked
-- TRUE  = opted in
-- FALSE = declined

ALTER TABLE players
  ADD COLUMN IF NOT EXISTS email_optin BOOLEAN DEFAULT NULL;

COMMENT ON COLUMN players.email_optin IS
  'Subscription opt-in shown after first feedback. NULL=not asked, TRUE=subscribed, FALSE=declined.';
