-- ── game_events ───────────────────────────────────────────────────────────────
-- Stores every significant in-game action for play-session debugging.
--
-- Notation format (the `notation` column):
--   E»MET_YUSUF@[D:met·FA:idl·FL:idl·O:idl·S:idl·B:idl·G:idl·M:idl·FC:0·hp:20/20·lv:1·c:5]
--   D»stunt_baert_fabric@[D:acc{137,170}·FA:acc·...]
--   I+fabric_bolt@[...]
--   I-flour@[...]
--   B»straatvechter:win+20xp+5c@[...]
--   M»borgerhout_east@[...]
--
-- State segment key (inside @[...]):
--   D   delivery arc   idl/met/acc{pkgs}/all/rwd
--   FA  fabric arc     idl/met/acc/pku/cmp
--   FL  flour arc      idl/acc/pku/cmp
--   O   oud arc        idl/acc/fnd/cmp
--   S   signatures     idl/col{fat,oma,...}/cmp/rwd
--   B   bulldozer      idl/vis/cmp
--   G   geest          idl/enc/cmp
--   M   mayor          idl/met/brf
--   FC  faction count  0–7
--   hp  current/max
--   lv  level
--   c   coins

CREATE TABLE IF NOT EXISTS game_events (
  id         bigserial    PRIMARY KEY,
  user_id    uuid         REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id uuid         NOT NULL,
  seq        int          NOT NULL,          -- ordering within a session
  ts         timestamptz  NOT NULL DEFAULT now(),
  notation   text         NOT NULL,          -- compact notation string (see above)
  raw_type   text         NOT NULL           -- 'xstate' | 'dialogue' | 'item' | 'battle' | 'map'
               CHECK (raw_type IN ('xstate','dialogue','item','battle','map')),
  raw_data   jsonb                           -- structured fields for querying
);

-- Index for "show me all events for user X in session Y, in order"
CREATE INDEX IF NOT EXISTS game_events_session_idx
  ON game_events (user_id, session_id, seq);

-- Index for recent-events queries across all users
CREATE INDEX IF NOT EXISTS game_events_ts_idx
  ON game_events (ts DESC);

-- Index for filtering by event type
CREATE INDEX IF NOT EXISTS game_events_type_idx
  ON game_events (raw_type, ts DESC);

-- ── Row Level Security ────────────────────────────────────────────────────────

ALTER TABLE game_events ENABLE ROW LEVEL SECURITY;

-- Users can only insert rows for themselves
CREATE POLICY "users_insert_own_events" ON game_events
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can read their own events (useful for self-debugging)
CREATE POLICY "users_read_own_events" ON game_events
  FOR SELECT
  USING (auth.uid() = user_id);
