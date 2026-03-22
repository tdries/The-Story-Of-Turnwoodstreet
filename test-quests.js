#!/usr/bin/env node
'use strict';

/**
 * Quest Sequence Tester — Turnhoutsebaan RPG
 *
 * Simulates the full quest chain mathematically: no browser, no Phaser.
 * Runs the same routing logic as OverworldScene.resolveDialogueId() and
 * the same quest-completion logic as QuestSystem.checkAll().
 *
 * Usage:  node test-quests.js
 */

const fs   = require('fs');
const path = require('path');

const DIALOGUE = JSON.parse(fs.readFileSync(path.join(__dirname, 'src/data/dialogue.json'), 'utf8'));
const QUESTS   = JSON.parse(fs.readFileSync(path.join(__dirname, 'src/data/quests.json'),   'utf8'));

// ── ANSI colours ─────────────────────────────────────────────────────────────
const G = '\x1b[32m', R = '\x1b[31m', Y = '\x1b[33m', B = '\x1b[36m', DIM = '\x1b[2m', X = '\x1b[0m';

// ── State ─────────────────────────────────────────────────────────────────────
let flags     = {};
let inventory = [];
let coins     = 5;
let _completedThisRun = [];

function reset() { flags = {}; inventory = []; coins = 5; _completedThisRun = []; }
const hasItem    = id  => inventory.includes(id);
const addItem    = id  => { if (!hasItem(id)) inventory.push(id); };
const removeItem = id  => { const i = inventory.indexOf(id); if (i !== -1) inventory.splice(i, 1); };

// ── Routing (mirrors OverworldScene.resolveDialogueId + conditionsMet) ───────
function conditionsMet(cond) {
  if (!cond) return true;
  if (cond.flags) {
    for (const [k, v] of Object.entries(cond.flags)) {
      if ((flags[k] ?? false) !== v) return false;
    }
  }
  if (cond.items)    { for (const id of cond.items)    { if (!hasItem(id)) return false; } }
  if (cond.notItems) { for (const id of cond.notItems) { if (hasItem(id))  return false; } }
  return true;
}

function resolveNode(npcId) {
  const candidates = Object.entries(DIALOGUE)
    .filter(([, node]) => node.npc === npcId && conditionsMet(node.conditions))
    .sort((a, b) => b[1].priority - a[1].priority);
  return candidates[0] ?? null;   // [nodeId, node] or null
}

// ── Dialogue execution ────────────────────────────────────────────────────────
/**
 * Execute a node's lines, applying all flag/item/coin effects.
 * choicePath: array of choice indices, consumed left-to-right when choices appear.
 * Returns { visited: string[], chosenLabels: string[] }
 */
function executeNode(nodeId, choicePath = []) {
  const path2 = [...choicePath];
  const node   = DIALOGUE[nodeId];
  if (!node) return { visited: [`MISSING:${nodeId}`], chosenLabels: [] };

  const visited      = [nodeId];
  const chosenLabels = [];
  let jumpTo         = null;

  for (const line of node.lines) {
    // Apply line effects
    if (line.flag       !== undefined) flags[line.flag]  = line.flagVal;
    if (line.flag2      !== undefined) flags[line.flag2] = line.flagVal2;
    if (line.item)       addItem(line.item);
    if (line.removeItem) removeItem(line.removeItem);
    if (line.coins)      coins += line.coins;

    // Handle choices
    if (line.choice && line.choice.length > 0) {
      const idx    = path2.shift() ?? 0;
      const chosen = line.choice[idx] ?? line.choice[0];
      chosenLabels.push(`[${idx}] "${chosen.label}"`);
      if (chosen.flag !== undefined) flags[chosen.flag] = chosen.flagVal;
      if (chosen.item)   addItem(chosen.item);
      if (chosen.coins)  coins += chosen.coins;
      if (chosen.next) { jumpTo = chosen.next; break; }
    }
  }

  if (jumpTo) {
    const sub = executeNode(jumpTo, path2);
    visited.push(...sub.visited);
    chosenLabels.push(...sub.chosenLabels);
  }

  return { visited, chosenLabels };
}

// ── Quest checks (mirrors QuestSystem.checkAll) ───────────────────────────────
function checkQuests() {
  const newlyDone = [];
  for (const q of Object.values(QUESTS)) {
    if (flags[q.completionFlag] === true) continue;
    if (!q.requiredFlags.every(f => flags[f] === true)) continue;
    if (!q.objectives.every(obj => flags[obj.checkFlag] === obj.checkValue)) continue;

    // Complete the quest
    for (const [k, v] of Object.entries(q.reward.flags)) flags[k] = v;
    for (const id of q.reward.items) addItem(id);
    coins += q.reward.coins;
    flags[q.completionFlag] = true;
    _completedThisRun.push(q.id);
    newlyDone.push(q.id);
  }
  return newlyDone;
}

// ── Test runner ───────────────────────────────────────────────────────────────
let pass = 0, fail = 0;

/**
 * Simulate talking to an NPC and assert outcomes.
 *
 * @param {string} npcId
 * @param {string} label       - human-readable description of this step
 * @param {object} opts
 *   choicePath   {number[]}  - choice indices to select at each branch (default: first choice)
 *   expectNode   {string}    - assert this specific node fires
 *   expectFlags  {object}    - assert each flag === value AFTER execution
 *   expectItems  {string[]}  - assert each item IS in inventory after
 *   notItems     {string[]}  - assert each item is NOT in inventory after
 *   expectQuests {string[]}  - assert these quest IDs complete as a result
 */
function talk(npcId, label, opts = {}) {
  const { choicePath = [], expectNode, expectFlags = {}, expectItems = [], notItems = [], expectQuests = [] } = opts;

  const result = resolveNode(npcId);
  if (!result) {
    console.log(`${R}✗${X} ${B}[${npcId}]${X} ${label}`);
    console.log(`    ${Y}! No matching node found — NPC '${npcId}' has no eligible dialogue${X}`);
    fail++;
    return;
  }

  const [nodeId] = result;
  const flagsBefore = { ...flags };

  const { visited, chosenLabels } = executeNode(nodeId, choicePath);
  const completed = checkQuests();

  const issues = [];

  if (expectNode && nodeId !== expectNode) {
    issues.push(`Expected node '${expectNode}', got '${nodeId}'`);
  }
  for (const [k, v] of Object.entries(expectFlags)) {
    if (flags[k] !== v) issues.push(`Flag '${k}': expected ${JSON.stringify(v)}, got ${JSON.stringify(flags[k])}`);
  }
  for (const id of expectItems) {
    if (!hasItem(id)) issues.push(`Expected item '${id}' in inventory`);
  }
  for (const id of notItems) {
    if (hasItem(id)) issues.push(`Item '${id}' should NOT be in inventory`);
  }
  for (const qId of expectQuests) {
    if (!completed.includes(qId)) issues.push(`Expected quest '${qId}' to complete`);
  }

  const ok = issues.length === 0;
  if (ok) pass++; else fail++;

  const icon   = ok ? `${G}✓${X}` : `${R}✗${X}`;
  const nodeStr = nodeId === expectNode || !expectNode ? `${DIM}${nodeId}${X}` : `${R}${nodeId}${X}`;
  console.log(`${icon} ${B}[${npcId}]${X} ${label} → ${nodeStr}`);

  if (chosenLabels.length) {
    console.log(`    ${DIM}choices: ${chosenLabels.join(' → ')}${X}`);
  }

  // Show flag changes
  const changed = Object.entries(flags)
    .filter(([k, v]) => flagsBefore[k] !== v)
    .map(([k, v]) => `${k}=${JSON.stringify(v)}`);
  if (changed.length) {
    console.log(`    ${DIM}flags: ${changed.join(', ')}${X}`);
  }

  // Show completed quests
  if (completed.length) {
    console.log(`    ${G}quests: ${completed.join(', ')}${X}`);
  }

  // Show issues
  for (const msg of issues) {
    console.log(`    ${Y}! ${msg}${X}`);
  }
}

/** Assert a flag value directly (no NPC talk needed). */
function assertFlag(key, expected, label) {
  const actual = flags[key] ?? false;
  const ok     = actual === expected;
  if (ok) pass++; else fail++;
  const icon = ok ? `${G}✓${X}` : `${R}✗${X}`;
  console.log(`${icon} ${label} (${key} = ${JSON.stringify(actual)})`);
  if (!ok) console.log(`    ${Y}! Expected ${JSON.stringify(expected)}${X}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
//  MAIN QUEST CHAIN
// ═══════════════════════════════════════════════════════════════════════════════

reset();

console.log(`\n${B}═══════════════════════════════════════════════════════════${X}`);
console.log(` Turnhoutsebaan RPG — Quest Sequence Tester`);
console.log(`${B}═══════════════════════════════════════════════════════════${X}\n`);

// ── Zone 1: Delivery ──────────────────────────────────────────────────────────
console.log(`${DIM}── Zone 1: Yusuf Delivery ──────────────────────────────────${X}`);

talk('yusuf', 'Meet Yusuf — accept delivery', {
  expectNode:  'yusuf_delivery',
  choicePath:  [0],   // "Ik help je met de laatste drie"
  expectFlags: { met_yusuf: true, delivery_accepted: true, delivery_packages_received: true },
  expectItems: ['delivery_package'],
});

talk('yusuf', 'Return to Yusuf — delivery complete', {
  expectNode:   'yusuf_delivery_done',
  expectFlags:  { delivery_done: true },
  expectItems:  ['tram_ticket'],
  notItems:     ['delivery_package'],
  expectQuests: ['q_starter_delivery'],
});

// ── Zone 1: Fatima + Fabric ───────────────────────────────────────────────────
console.log(`\n${DIM}── Zone 1: Fatima & Fabric ─────────────────────────────────${X}`);

talk('fatima', 'Meet Fatima — accept fabric quest', {
  expectNode:  'fatima_intro',
  choicePath:  [0],   // "Ik kan die stof voor je halen"
  expectFlags: { met_fatima: true, fabric_quest_accepted: true },
});

talk('fatima', 'Second talk — confirm Baert location', {
  expectNode:  'fatima_fabric_accept',
  expectFlags: { knows_stunt_location: true },
});

talk('baert', 'Visit Baert — pick up fabric', {
  expectNode:  'stunt_baert_fabric',
  expectFlags: { stunt_quest_active: true },
  expectItems: ['fabric_bolt'],
});

talk('fatima', 'Deliver fabric to Fatima → community trust', {
  expectNode:   'fatima_after_fabric',
  expectFlags:  { stunt_quest_done: true, has_community_trust: true },
  notItems:     ['fabric_bolt'],
  expectQuests: ['q_fabric_quest'],
});

// ── Zone 1: Omar flour ────────────────────────────────────────────────────────
console.log(`\n${DIM}── Zone 1: Omar Flour ──────────────────────────────────────${X}`);

talk('omar', 'Talk to Omar — flour request', {
  expectNode:  'omar_flour_request',
  choicePath:  [0],   // "Ik haal het voor je"
  expectFlags: { omar_flour_asked: true, flour_quest_accepted: true },
});

talk('yusuf', 'Budget Market — buy flour (npc=yusuf, priority 110 > yusuf_done 100)', {
  expectNode:  'budget_market_flour',
  expectFlags: { has_flour: true },
  expectItems: ['flour'],
});

talk('omar', 'Return flour to Omar', {
  expectNode:   'omar_flour_done',
  expectFlags:  { omar_flour_done: true },
  notItems:     ['flour'],
  expectQuests: ['q_flour_shortage'],
});

// ── Zone 2: Reza oud quest ────────────────────────────────────────────────────
console.log(`\n${DIM}── Zone 2: Reza Oud String ─────────────────────────────────${X}`);

talk('reza', 'Meet Reza — accept oud quest', {
  expectNode:  'reza_music',
  choicePath:  [0],   // "Ik zoek die snaar voor je"
  expectFlags: { oud_quest_accepted: true },
});

talk('aziz', 'Aziz gives oud string', {
  expectNode:  'aziz_oud_string',
  expectFlags: { has_oud_string_item: true },
  expectItems: ['oud_string'],
});

talk('reza', 'Give oud string to Reza', {
  expectNode:   'reza_oud_found',
  expectFlags:  { reza_quest_done: true },
  notItems:     ['oud_string'],
  expectQuests: ['q_oud_string'],
});

// ── Zone 2: Signatures ────────────────────────────────────────────────────────
console.log(`\n${DIM}── Zone 2: Signatures ──────────────────────────────────────${X}`);

talk('fatima', 'Get Fatima\'s signature', {
  expectNode:  'fatima_signature',
  expectFlags: { sig_fatima: true },
});

talk('omar', 'Get Omar\'s signature', {
  expectNode:  'omar_signature',
  expectFlags: { sig_omar: true },
});

talk('reza', 'Get Reza\'s signature (bug: reza_done priority 100 used to block this)', {
  expectNode:  'reza_signature',
  expectFlags: { sig_reza: true },
});

talk('baert', 'Get Baert\'s signature', {
  expectNode:  'stunt_baert_signature',
  expectFlags: { sig_baert: true },
});

talk('aziz', 'Get Aziz\'s signature', {
  expectNode:   'aziz_signature',
  expectFlags:  { sig_aziz: true },
  expectQuests: ['q_signatures'],
});

assertFlag('speculator_threatened', true, 'Speculator threatened (q_signatures reward)');

// ── Post-signature NPC states ─────────────────────────────────────────────────
console.log(`\n${DIM}── Post-signature NPC states ────────────────────────────────${X}`);

talk('reza', 'Reza post-sig → reza_done fires correctly', {
  expectNode: 'reza_done',
});

talk('yusuf', 'Yusuf post-flour → yusuf_done fires (not budget_market_flour)', {
  expectNode: 'yusuf_done',
});

talk('omar', 'Omar post-sig → bakker fallback', {
  expectNode: 'omar_bakker',
});

// ── Zone 3: El Osri ───────────────────────────────────────────────────────────
console.log(`\n${DIM}── Zone 3: El Osri / Borger Hub ────────────────────────────${X}`);

talk('el_osri', 'Talk to El Osri → visited_de_roma + met_mayor', {
  expectNode:  'district_mayor',
  choicePath:  [0],   // "Ja. Ik doe mee."
  expectFlags: { met_mayor: true, visited_de_roma: true, act4_started: true },
});

// ── Regression: met_mayor before all sigs ────────────────────────────────────
// Simulates a player who wandered into zone 3 before collecting Fatima's sig.
// fatima_faction (80) and fatima_all_done (70) must NOT fire when sig_fatima=false.
console.log(`\n${DIM}── Regression: zone-3 access before Fatima's signature ─────${X}`);
{
  const savedFlags = { ...flags };
  // Inject met_mayor=true as if player talked to El Osri before all sigs
  flags.met_mayor = true;
  flags.sig_fatima = false;  // pretend we haven't got her sig yet

  talk('fatima', 'Fatima with met_mayor=true but sig_fatima=false → must give signature', {
    expectNode:  'fatima_signature',
    expectFlags: { sig_fatima: true },
  });

  // Restore — continue as if this branch never happened
  Object.assign(flags, savedFlags);
  flags.sig_fatima = true;  // mark it done for next tests
}

// ═══════════════════════════════════════════════════════════════════════════════
//  SUMMARY
// ═══════════════════════════════════════════════════════════════════════════════

console.log(`\n${B}═══════════════════════════════════════════════════════════${X}`);
if (fail === 0) {
  console.log(`${G} ✓ All ${pass} tests passed — quest chain flows correctly!${X}`);
} else {
  console.log(`${R} ✗ ${fail} test(s) failed${X}, ${G}${pass} passed${X}`);
}
console.log(`  Completed quests: ${_completedThisRun.join(', ') || '(none)'}`);
console.log(`${B}═══════════════════════════════════════════════════════════${X}\n`);

if (fail > 0) process.exit(1);
