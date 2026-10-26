# Xenogears Disc 2 REDO — Design Bible

A playable second disc for [Weltall](https://github.com/Roman215/Weltall), built as a
story pack (plain-text documents under `Content/Story/`). Every narrated "chair" section
of the original Disc 2 becomes a played sequence that branches from the original game and
rejoins it with the same saved state, using Weltall's story toolkit.

This document is the source of truth for scope, canon decisions and build order. The
pack files live in `pack/` (mirrors `Content/Story/disc2-redo/` in Weltall).

---

## 1. What we are fixing

Disc 2 of Xenogears (1998) tells most of its second half through narration: Fei, Elly and
Citan sit in a dark room and describe events over still images while the player presses
confirm. Only a handful of dungeons (Anima dungeons, Merkava, Zohar cave, Deus) and the
boss fights are played.

Takahashi's own account (Kotaku, 2017): Square wanted to end the game at the Solaris
escape. He proposed the narrated disc so the story could be finished with the remaining
staff, time and budget. In Perfect Works he says only about a third of the full story made
it in. Nothing official lists which Disc 2 scenes were meant to be played. Everything
below that goes beyond the script is design, labelled as such.

## 2. Principles

1. **Canon first.** Every plot beat, line of exposition and character fate from the
   original Disc 2 stays. Narration is converted, not rewritten. Where the chair script
   already contains dialogue (Elly at the Soylent facility, Ramsus at Nisan, the Mahanon
   argument), that dialogue is staged as the scene it describes, and quoted by reference
   (`message X from map 617 message N`, an engine addition) so the scene speaks whichever
   script the player runs: the original's or Perfect Works Build's retranslation.
2. **Play what was told.** The default conversion for a narrated paragraph is: a map, the
   party walking through it, NPCs with lines, a trigger, a battle that already exists on
   the disc, then the original cutscene or Gazel scene.
3. **The game's own assets first.** Weltall cannot import models or FMV. Every new map reuses
   an existing map's geometry; every boss is an existing battle formation; every "cutscene"
   is an in-engine scripted scene. Sprites a map lacks are borrowed from the disc map that
   has them (`sprite N from map K slot S`, an engine addition carried in `engine/` and in
   the upstream PR); Gears are global models (`SetGearModel`). New art is made only for
   things no disc holds, and goes in through Weltall's texture replacement (a PNG per
   original texture or sprite sheet, same cell layout).
4. **NPC dialogue is the texture.** Disc 1 is dense with talk-to-anyone lines. Each town
   revisit here gets a full NPC pass that reflects the state of the world (mutations,
   Nisan refugees, the peace treaty, the war).
5. **Rejoin exactly.** Each sequence ends by restoring the story value, flags, map and
   entrance the original script expects, so Weltall's `[Story]` tests pass and saves stay
   compatible with the unexpanded game.
6. **Respect over spectacle.** One or two twists, both drawn from what the script already
   sets up (see §8). No new villains, no retcons.

## 3. Sources

| Source | Used for |
|---|---|
| Disc 2 game script (GameFAQs, Sheamon) | Every narrated beat, verbatim lines, scene order |
| Weltall `Docs/Story/*` and `Content/Story/disc2/*` | Toolkit, syntax, worked examples (rematch, Mass Driver) |
| Kotaku, "The Real Story Behind Xenogears' Unfinished Disc 2" (2017) | Why the disc is narrated |
| xenogearsxenosagastudyguide (translation-errors guide, Disc 2) | Chapter list 56–68; corrected meanings for Miang/Elhaym/Krelian/Zohar lines |
| r/XenoGears, "Xenogears Disc 2: Original Plan?" (2024) | Fan consensus on which sections were dungeons; disputed items |
| Perfect Works (via study guide) | Episode V framing; "a third of the story" |

### Fan consensus we adopt (top-voted, lore-consistent)

- Mass Driver was a dungeon (Weltall already built it).
- Soylent System facility with the Sufal Mass was a dungeon.
- Mahanon was more than one hallway.
- Bart's trip to Nortune for the Yggdrasil IV was its own sequence (the OP's wish).
- Ramsus' assault on Nisan and Elly's flight to Golgoda were scenes, not slides.
- The area around Zohar and the Merkava assault were played (they partly are).
- Loose threads worth closing: Sigmund and Rico, Jessie and Yui, Ramsus' fate, the
  Elements, Margie.

### Fan claims we do not adopt

- Omnigears for Maria and Emeralda. Perfect Works says a design existed; the game's own
  lore (Animus ratings, Emeralda is not an Animus, Seibzehn carries a human brain) and the
  Gazel line that all twelve Relics are accounted for make it incoherent. Not canon here.
- Ramsus, Margie or Dominia as party members. Weltall's party is the disc's eleven
  characters; the engine has no slot for more. Ramsus gets a scripted ally role instead.

## 4. Engine toolkit and hard limits

From `Docs/Story/README.md` and the guides:

| Document type | What it does | We use it for |
|---|---|---|
| `map N` | Patch an existing map's scripts/messages | Branch points, NPC lines in towns, rejoin edits |
| `map 730..1023 from K` | New map on K's geometry, all-new scripts | Dungeon rooms, new scenes |
| `map 730..1023 over K` | New map on K's geometry and scripts, patched | Reusing a staged scene (sky, bridge, throne) |
| `battle event N` | Trim narration before a battle, add a transition page | Every boss that keeps its narration |
| `world map 8` | New locations, arrival points, hide the ship | Soylent sites, Nortune, Golgoda, Taura's |
| `way back` | Save fallback for new story values | Every new story value |
| `subtitles` | "Chapter 57a: …" cards inside original chapters | One per sequence |

Hard limits to design around:

- New maps reuse existing geometry only; map IDs 730–1023 are free (294 slots).
- No new FMV; a replacement movie must keep sector layout. All cutscenes are in-engine.
- No new minimap dots (dots 14, 19, 21, 22 are unused and available; 21 is used by the
  Mass Driver).
- New world-map locations use the region's existing encounter table.
- Message windows: 35 letters per line (26 with portrait), 4 lines per page. Narration
  pages: 24 letters, 4 lines. Subtitles: 24 letters.
- Party size and roster are the disc's. Party changes are scripted (`PartyAdd`/`PartyRemove`).
- Story progress is `var[000]`; each sequence takes an unused value and maps back via
  `way back`.
- Some disc data stays loaded; a few changes need a restart. Tests catch mismatches.

Verification available to us: `WeltallMapText` listings (needs the disc images), the
`[Story]` test tag, and the `RenderScreen` commandlet for headless screenshots/video.

## 5. The original Disc 2, beat by beat

Chapters 56–68 per the save-slot titles. "Chair" = narrated; "Played" = already playable.

| Ch. | Title | Beat | Original form |
|---|---|---|---|
| 56 | Shot Down! | Lacan/Sophia dream; Fei wakes at Taura's; the Limiter plan; Shevat emissary; party splits; Grahf recognises Lacan; Gazel scene; Ramsus rematch | Dream and Taura's house played; rematch chair → battle |
| 57 | Break The Seal | Elly + Emeralda to Mass Driver; Nisan defence; Nortune; Yggdrasil IV vs Mobile Weapon; nanomachines spread; mutations begin; Krelian's virus | Chair |
| 57 | (cont.) | Soylent System: Wels, Sufal Mass, Elly's blood and speech; Nisan nursing; "second Sophia"; Gazel key; Cain forbids | Chair with staged dialogue |
| 58 | Soul Vessel | Anima dungeon (Billy); Elements in Union; Gazel plot Cain's death; Ramsus unravels | Played dungeon, chair bridges |
| 58 | (cont.) | Elly returns to Nisan; Ramsus assaults Nisan; Elly stops him; Gazel reject Ramsus; Krelian/Miang turn him | Chair with staged dialogue |
| 59 | The Stars Know | Anima dungeon (Rico); Hammer boss and death | Played |
| 60 | Above Mahanon | Ramsus beheads Cain; Gaetia Key; Wels howl; Mahanon rises; Fei/Elly argument and night; pendant; Margie on the bridge | Cutscenes + chair |
| 61 | Paradise | Mahanon interior; rotting nucleus boss; Razael's Tree; Grahf defeats the party; "crucify them at Golgoda" | One hallway played, rest chair |
| 62 | Promised Land | Pendant breaks; Elly to Shevat; her troops; Golgoda duel vs Rattan and Mugwort; Elly taken; Krelian erases the Gazel | Chair with staged dialogue |
| 63 | Waiting Death | Wiseman's lesson; two-week search; Elements at Merkava; Merkava dungeon; Ramsus (Bladegash); Krelian's lab; Opiomorph; Deus takes the Relics; Ramsus kills Miang; Elly shoots Fei; "I am Miang"; Deus rises | Played (Merkava) |
| 64 | Merkava Calls | Seraphs devastate the surface; Fei found and frozen; Zephyr's confession; Lacan/Sophia/Krelian flashbacks; Dan and Midori; Id breaks out | Chair + flashback cutscenes |
| 65 | Dreams... | Zohar cave; Id boss; Wiseman is Khan; Fei's childhood; Karen as Miang; the Coward; the Wave Existence; Xenogears; Grahf-in-Khan boss; Kadomony | Played |
| 66 | Fallen Star | Excalibur war room; Taura's disassemblers; Bart's ramming plan; Merkava destroyed; Deus' final form | Cutscene + chair |
| 67 | Xenogears Wakes | Sidequests: Zephyr in the snow; Ramsus revived; Taura's farewell; Lighthouse / Zeboim city / Kim and Emeralda; Emeralda grows | Played, optional |
| 68 | First And Last | Deus; orbs; Zohar stops; Deus lifts; Fei alone; Krelian; Elly freed; return | Played |

## 6. The REDO, sequence by sequence

Each sequence names: branch point, new maps (base geometry to reuse), battles (existing
formations), rejoin, loose ends it closes. Sizes are T-shirt (XS–XL).

Story values: Weltall's examples use 253 (Mass Driver). We reserve unused values in the
250–299 band per sequence; exact numbers are assigned after reading the disc's chapter
file with `WeltallMapText` and `FChapterTitles`, because each must fall inside the right
original chapter for the subtitle card to number itself correctly.

### R0. Already built upstream — adopt as-is

- **Ramsus rematch above the forest** (`rematch-*.txt`).
- **Elly and Emeralda to the Mass Driver** (`mass-driver-*.txt`, three rooms, control room
  with Citan, launch).

We keep these files unchanged and start after them. Size: none.

### R1. Chapter 57a — "Four Hours To Nisan" (Fei's side)  — Size M

Narrated: "After we pushed back the Solarian Gear units, we headed for Nortune…"

- **Branch:** after the rematch aftermath, instead of returning to the chair, Fei lands at
  Nisan (reuse Nisan map set from Disc 1, Ch. 44 "Protect Nisan!" staging).
- **Play:** a short Gear defence of Nisan's approach against Solarian units (reuse the
  Ch. 44 soldier formations), then Bart's briefing in the Cathedral.
- **NPC pass:** Nisan sisters, refugees from Bledavik ("half the city is gone"), Margie.

### R2. Chapter 57b — "Secret Battleship" (Nortune)  — Size L

Narrated: Nortune's Central District is Roni Fatima's hidden battleship; Bart activates it.

- **Maps:** Nortune (Disc 1 Kislev capital maps: A/B/C/D blocks, Imperial Palace).
  New "under the Palace" rooms on Zeboim/Solaris facility geometry (`from`), 2–3 rooms.
- **Play:** Rico leads the party into Nortune under curfew. Sigmund refuses, then yields
  when Hammer's old network (now Rico's) produces Roni's records from the Battling
  archive. Puzzle: raise the district (three control rooms, in any order).
- **Loose end closed:** Rico and Sigmund. Sigmund acknowledges Rico publicly on the
  bridge before the launch. (Hammer's later "you are next in line to be Kaiser" then
  lands.)
- **Battle:** Yggdrasil IV vs the Mobile Surface Supremacy Weapon as a scripted
  cutscene (the script treats it as a one-line win); no new formation needed.
- **Rejoin:** sets the flags the original sets when the narration passes "peace was
  signed", returns to the chair at the nanomachine-dispersal page via `battle event`-style
  page skip or a direct map change into the next sequence.

### R3. Chapter 57c — "The Howling" (mutations and the Soylent System)  — Size XL

The biggest conversion and the heart of the redo.

- **Maps (as built):** the facility is the disc's own cut dungeon: Disc 2 maps 621 (gate
  hall), 620 (holding hall, Wels with empty talk scripts) and 622 (the tank room with the
  Sufal Mass's breakout scripted) are walkable; R3's rooms 742/743/744 are `from` them,
  so nothing is borrowed from Ethos or Zeboim and no art is made. Three rooms in v1: gate
  hall (Citan names the place; seven Wels with lines), holding hall (a Gebler soldier of
  Elly's Bledavik unit asks the "haves" question to her face), the processing line (the
  queue for the tank; the System goes out of control; the original's own breakout script).
- **Play:** the party (Fei, Elly, Citan + one) enters at the request of a Nisan refugee
  whose family "went to be saved". Talk-to-everyone lines are the "haves and have-nots"
  exchange from the script, now as NPC dialogue rather than Elly's summary.
- **Battle:** the Sufal Mass (existing formation). Then Elly's blood scene and her speech
  to the mutated — staged with the Sophia overlay lines exactly as scripted.
- **Second and third sites:** the script says "we went from place to place". We add two
  world-map locations (reuse the Sargasso and Ignas desert ruin geometry) with short
  2-room variants and no boss, optional, each adding Nisan refugees. Mild side content,
  not required.
- **Interleaved cutscenes (unchanged):** Krelian's virus, Gazel key, Cain forbids.
- **NPC pass, Nisan:** the clinic; Margie; Yui treating patients (loose end: Yui alive —
  this is where the game itself places Midori saying so); Jessie repairing the orphanage
  wall. Sets up Billy's "Jessie Blasta" the way the game unlocks it later.
- **Rejoin:** chapter 58 start, Anima dungeon as original.

### R4. Chapter 58a — "Gold In The Fire" (Ramsus assaults Nisan)  — Size M

Narrated with full dialogue; one of the best scenes in the game, told over four stills.

- **Branch:** when Elly leaves the party before the second Anima dungeon.
- **Play as Elly:** Nisan under attack. Walk through burning Nisan (reuse Ch. 44 ruined
  staging) past Renk and the Solarian deserters holding the line; reach the Cathedral.
- **Battle:** Vendetta vs Elly on foot is not winnable and the script says she stops him
  with ether. Staged as a scripted "battle" that ends on page 1 (Weltall's `battle event`
  lets us cut in), then the full Ramsus/Elly exchange as dialogue with the Krelian/Karen
  still replaced by the in-engine lab scene from Ch. 63 (geometry exists).
- **Rejoin:** Gazel "trash" scene, Krelian and Miang turning Ramsus, back to Fei's party at
  the Rico dungeon.

### R5. Chapter 60a — "The Night Before" (Nisan, Mahanon eve)  — Size S

Already dialogue, shown as a cutscene. We make it a walkable evening in Nisan: the
Yggdrasil crew's lines (Bart, Citan, Margie, Billy, Maison, Emeralda) become NPC talk,
the Fei/Elly scene stays verbatim, the morning and the pendant stay verbatim. Adds the
Margie/Elly bridge conversation as a place you walk to.

### R6. Chapter 61 — "Mahanon" (full dungeon)  — Size L

The game plays one hallway. The script describes: interceptor battle, control room,
the rotting nucleus, Razael's cavern.

- **Maps:** the existing Mahanon hallway `over` plus 3–4 new rooms on Eldridge-looking
  geometry (the intro-movie ship is not a field map; use Solaris/Zeboim machine
  interiors and the Merkava core-room geometry for the Razael cavern).
- **Battles:** existing nucleus formation; Grahf's scripted loss stays a loss.
- **Rejoin:** Krelian's "Golgoda" line, Elly's pendant scene.

### R7. Chapter 62 — "Golgoda" (Elly alone)  — Size M

- **Play as Elly:** Shevat hangar scene with Renk, Helmholz, Stratski, Vance, Broyer as
  NPCs (their lines exist verbatim). Fly El-Regrs to a new world-map location "Golgoda"
  (reuse the crucifix field geometry from the existing Golgoda scene map).
- **Battle:** Rattan and Mugwort, existing formations, solo Elly in her Omnigear. The
  script has her lose, stand, and win; we script a two-phase fight: phase one ends on a
  scripted KO, phase two is the real fight.
- **Rejoin:** Krelian takes her; Grahf's taunt; Gazel erasure cutscene.

### R8. Chapter 63 — Merkava: keep, plus "Dominia's Door"  — Size S

The dungeon is played already. One addition: the Elements' separate route (Dominia
appears from "another entrance") becomes a short optional corridor the player can take
with Dominia as a scripted NPC escort, giving the Elements their stated motive on screen.

### R9. Chapter 64 — "Fallen Star" (Shevat after Merkava)  — Size M

Narrated by Citan: Seraphs devastate the surface; Fei found; carbonite; Zephyr's
confession; Dan and Midori.

- **Play:** Shevat in decline (reuse Shevat maps, lights off, fewer NPCs). Citan can
  talk to Zephyr (confession as dialogue), Maria, Emeralda, Dan, Midori, Yui, Taura
  (relocated). The Lacan/Sophia flashbacks stay as the game's own cutscene chain.
- **Loose end closed:** Jessie and Yui in one place at last; Billy's reconciliation beat.
- **Rejoin:** Id breaks out, party pursues to the snowfield — original Ch. 65 unchanged.

### R10. Chapter 66 — "Excalibur" (the ramming operation)  — Size M

- **Play:** the war-room is already a cutscene; we add a walkable Excalibur (reuse
  Yggdrasil bridge/hangar geometry) where the whole surviving cast, the Elements, Ramsus
  (recovered — the sidequest scene moved before the assault, where it belongs), Taura and
  Zephyr have pre-battle lines.
- **Battle:** the approach as a played Gear fight against Seraphs (existing formations)
  while the ships run their timer, then the ramming as the original cutscene.
- **Loose end closed:** Ramsus fights alongside, as scripted ally in the approach cutscene.

### R11. Chapter 68 + epilogue — "Tomorrow"  — Size M

The final dungeon and Deus are unchanged. After the credits' return shot, a short
playable epilogue on the seashore and in Nisan (see §8 for its two twists):

- Each party member has a farewell line (Bart's "partner" promise paid off).
- Fei and Ramsus spar, "in sport, not war", as the script promises — a single
  friendly battle using an existing on-foot Ramsus formation, unlosable.
- The pendant resolved (§8).
- Final subtitle card, then the original credits remain the real ending; the epilogue
  is entered from a post-credits prompt so purists keep the 1998 ending untouched.

## 7. Loose ends and how each is closed

| Thread | Where | How |
|---|---|---|
| Sigmund and Rico | R2 Nortune | Sigmund yields the Palace; acknowledges Rico before the launch. |
| Hammer's "next Kaiser" | R2 → original Ch. 59 | Now foreshadowed by R2. |
| Jessie and Yui | R3 Nisan clinic, R9 Shevat | Yui alive and nursing (consistent with Midori); Jessie present; Billy's "Jessie Blasta" unlock is where the game puts it. |
| Ramsus | R4, R10, R11 | Nisan scene played; recovery moved before the Excalibur run; friendly bout in the epilogue. |
| The Elements | R8, R10 | Their own motive on screen; survive and fight. |
| Margie | R1, R3, R5 | Nisan's acting Mother while Elly is away; her lines all exist. |
| Dominia and Maria | R9 | One exchange in Shevat closing the Seibzehn story. |
| Emeralda | original Ch. 67 | Unchanged; the Lighthouse sidequest stays optional. |
| Taura | R9 | Dies as the script implies, with the farewell lines in place. |

## 8. The two twists (both already in the script)

1. **The pendant is Karen's.** The game shows the Nisan pendant on Karen when she dies,
   then Fei finds it at Zohar and asks "Sophia's… or my mother's?" and never answers.
   Epilogue: Elly, who now carries every Miang's memories, recognises it — Karen wore it
   because Sophia had, and Karen chose to keep it. The object that Fei asked Elly to hold
   before Mahanon was his mother's. No new lore; a question the game asks gets its answer.
2. **No more Miang.** Karen's "the final one", the Wave Existence's release of
   Elhaym, and Grahf's "Save her and all the other women bound with her" are read by most
   players as: the cycle ends. The epilogue confirms it in one line from Elly — the voice
   is gone, and it will not wake in anyone else — delivered quietly, not as a reveal.

Nothing else is added to the ending. Krelian's departure, Deus' removal, Zohar's end and
the loss of Gears and Ether all stand.

## 9. File layout

Weltall gates exactly one pack folder, `Content/Story/disc2`, on the player's "Extended"
choice (`FStoryPacks::ExpansionPack = "disc2"`); any other folder's documents apply to every
game, and the `way back` and `subtitles` documents must be that pack's, one each. So the
redo's documents live **inside** `disc2/`, beside Roman215's rematch and Mass Driver files,
with a sequence prefix in their names, and extend his `subtitles.txt` and `way-back.txt`.

```
pack/                          → Content/Story/disc2/ in Weltall (added or changed files only)
  subtitles.txt                his, plus one `story` line per sequence
  way-back.txt                 his, plus one row per new story value
  nisan-assault-parting.txt    R4: the branch in the chair (map 617)
  nisan-assault-town.txt       R4: map 740 from 93
  nisan-assault-cathedral.txt  R4: map 741 from 95
  soylent-*.txt                R3 …
tests/                         → Tests/WeltallCore/Story/ in Weltall, one file per sequence
docs/
  DESIGN-BIBLE.md              this file
  MAP-REGISTER-disc2.md        the 205 field maps Disc 2 holds (generated)
  STORY-VALUES.md              chapter table; values each sequence takes
```

## 10. Build order and gates

Each step is gated by Weltall's `[Story]` tests against the discs and a `RenderScreen`
capture of the new scene.

1. **Scaffold (XS):** pack folder, subtitles, way-back, docs register; a one-room smoke
   map to prove the pack loads in a `--expansion` build.
2. **R4 Nisan assault (M):** small, self-contained, all dialogue exists; proves the
   "play as Elly" pattern and `battle event` cut-ins.
3. **R3 Soylent (XL):** the showcase. Needs the most new rooms and the NPC pass.
4. **R2 Nortune (L):** the fan-requested chapter; big NPC pass.
5. **R6 Mahanon, R7 Golgoda (L + M).**
6. **R1, R5, R9, R10 (town/ship passes).**
7. **R8, R11 (epilogue last; it depends on everything).**

## 11. Distribution

- Players copy `pack/` into `<Weltall>/Weltall/Content/Story/disc2-redo/` of a build made
  with `--expansion`, or a stock build if upstream agrees to load extra packs from the
  package folder (Weltall reads `Content/Story` at startup, so a stock build may already
  pick it up; verify on 0.8.x).
- Upstream PR: a branch on a fork of Roman215/Weltall adding the files to
  `Content/Story/disc2/` and a test per sequence. Opened once step 2 above passes the tests, so
  the first PR is reviewable and runnable rather than a design document.
- Platforms: Windows and Linux (Weltall's). Android is not reachable with Weltall today;
  Quiver Launcher on Android installs APKs only.

## 12. Open questions for Mark

1. Location of the USA disc images (BIN/CUE or CHD) so `WeltallMapText` listings and the
   `[Story]` tests can run; nothing below step 1 can be verified without them.
2. Should the optional Soylent sites (R3, two extra facilities) be in scope for v1, or
   deferred?
3. Epilogue (R11) as a post-credits prompt (default) or as a mandatory scene before the
   credits?
