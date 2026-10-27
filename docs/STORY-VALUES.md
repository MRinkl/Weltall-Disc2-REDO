# Story values (event variable 0) — Disc 2 chapters

From the USA Disc 2 chapter-title file, read with Weltall's `FChapterTitles` (first story
value of each chapter). Chapter numbers are the save-slot ones.

| Ch. | First value | Title |
|---|---|---|
| 56 | 249 | Shot Down! |
| 57 | 252 | Break the Seal |
| 58 | 263 | Soul Vessel |
| 59 | 281 | The Stars Know |
| 60 | 285 | Above Mahanon |
| 61 | 288 | Paradise |
| 62 | 290 | Promised Land |
| 63 | 295 | Waiting Death |
| 64 | 298 | Merkava Calls |
| 65 | 310 | Dreams... |
| 66 | 325 | Fallen Star |
| 67 | 330 | Xenogears Wakes |
| 68 | 340 | First and Last |

Weltall's `disc2` pack uses **253** (Mass Driver, inside chapter 57). Its subtitles use
254 and 258 as card starts inside chapter 57.

## Reserved for this pack

A sequence's new value must lie inside the chapter it plays in, so its subtitle card
numbers itself under the right chapter. Values are reserved once the original scripts of
both discs have been scanned for every value they set and test (needs Disc 1 in `Games`).

| Seq. | Chapter | Value | Status |
|---|---|---|---|
| R4 Nisan assault (Elly) | 58 (263–280) | **269** | done, tests pass. The session plays at 268 (Weltall's own subtitle "Holy Mother Returns" sits there). Branch: map 617, entrance 3, `@0x0890 StartScriptWaitEnd actor31 script12@1`; rejoin: story 268, party Fei, 9, Elly, `ChangeMap #273 #12` |
| R3 Soylent facility (Fei, Elly, Citan) | 57 (252–262) | **259** | done; play test passes. Branch: map 673 (Krelian's lab), entrance 1, `@0x0237 ChangeMap #621 #0`; rooms 742 (from 621), 743 (from 620), 744 (from 622); rejoin: story 258, `ChangeMap #622 #1` (the fight entrance: prep menu, Sufal Mass, Elly's blood and speech, all original). No disc script tests 258–262. |
| R2 Nortune (Fei, Bart, Rico) | 57 (252–262) | **254** | done; play test passes. Weltall's own subtitle "Secret Battleship" already sat at 254, so the card needs no new line. Branch: map 618 (Fei's chair), entrance 0, session 1, `@0x0740 ChangeMap #198 #8` (after the save prompt and `SetVarBit var[248] #2`); rooms 745 (from 198, the gate under curfew), 746 (from 237, the Kaiser's hall), 747 (from 231, the tactical command room: three stations, any order), 748 (from 234, the bridge); rejoin: `PartyRemove 3/5`, story 252, `ChangeMap #198 #8` (the original's scene: the rising narrated, Battle 8, back to the chair's session 2). Way back: 254 → map 198 entrance 8 at 252. No disc script tests 253–257. |
| R1 Nisan defence | 57 (252–262) | TBD | |
| R5 Mahanon eve | 60 (285–287) | TBD | chair map 617 → `ChangeMap #303 #3` |
| R6 Mahanon (Fei, Citan, Bart) | 61 (288–289), 62 (290–294) | **289**, **291** | done; play tests pass. The chain enters at 288 (set by map 672, the pendant dream): 652 approach → 653 flight (narrated, save prompt) → 654 hallway (played; nucleus Battle 12; `SetAcc #290`) → 655 cavern scene (narrated; Krelian; Grahf Battle 13) → 656. Wreck: map 652 `@0x0108 ChangeMap #653 #0` → 749 (from 653) at 289 → `ChangeMapTransition #17038 #0 #0 #32` (654, as the flight enters it) at 288. Cavern: map 654 `@0x5019 ChangeMap #655 #0` → 750 (from 655) at 291 → `ChangeMap #655 #0`, where a detour at `@0x074B` (msg6) skips the three pages the walk said and restores 290. Map 619 is not Mahanon: it is another chair map (sessions by entrance). No disc script sets 289 or tests 286–294. |
| R7 Golgoda (Elly alone) | 62 (290–294) | **292** | done; play test passes. Weltall's own "Elly's Decision" card already sat at 292. The original: 656 (Grahf after the cavern) → 493 (Elly nursing in Nisan, Margie) → 617 #5 (Elly's chair: two nine-line pages, msg58–59; her unit's farewell msg60–84 over stills; `ChangeMap #657 #0`) → 657 (the Shevat hangar as a silent camera flight) → 619 #3 (Golgoda: Krelian's offer msg31–48, Elly's choice, Battle 14; then the stills after, party Fei/Citan/Bart, `ChangeMap #273 #14`). Branch: map 617 `@0x1BD0 StartScriptWaitEnd actor11 script5@1` (after the two pages); room 751 (from 164: the hangar map that has Renk's unit's sprites; 657's own floor cannot show text on a map of its own, see the engine rules); rejoin: `GearMode 1; SetSlotInGear 0..2`, story 290, `ChangeMap #619 #3`. The Golgoda confrontation and battle stay the chair's: they are already dialogue. |
| R9 Shevat aftermath | 64 (298–309) | TBD | |
| R10 Excalibur | 66 (325–329) | TBD | |
| R11 Epilogue | 68 (340+) | TBD | |

## Disc 2 scene-chain maps (from the register)

- 617: the chair (Fei/Elly), 8 entrances = 8 narration sessions; jumps to 273, 303, 616, 618, 657, 670, 728
- 618: chair continued (Yggdrasil IV, Soylent lead-in), jumps to 198, 290, 515, 659, 687, 698, 709
- 619: Mahanon narration; 620–625: Soylent narration backgrounds; 670: the Lacan/Sophia dream
- 273: SOL-9000 / Gazel Ministry and Krelian scenes (15 entrances)
- 303: the night before Mahanon (Yggdrasil); 290/296/301/302: Yggdrasil rooms
- 164: Shevat hangar, Elly leaves for Golgoda; 656: Golgoda aftermath (Grahf); 650: Hammer; 653/655: Mahanon interior; 714: Merkava core
- 728: the debug/menu map (567 messages), not for use

## How Disc 2 scripts use progress (verified on the USA Disc 2 listings)

- Field scripts on Disc 2 never write `var[000]`; they test it through the accumulator
  (`IfAccEqual #N`, `IfAccGreater #N`), which holds the progress at script start. Weltall's
  own documents write it with `SetVar var[000] #N`.
- Values Disc 2 field scripts test: 279–283, 298–306, 320, 330, 339, 340, 349, 350 (plus
  Disc 1 values on maps both discs share). Inside chapter 58 (263–280) only 279 and 280 are
  tested on Disc 2, so R4's value will come from 264–278 once Disc 1's maps are scanned too.
- The chair's sessions are picked by entrance (`var[002]`) on map 617, not by progress, and
  flags in `var[248]` (bits 2, 3, 4, 8) mark which sessions have been seen. A sequence that
  replaces a session must leave those bits as the session would.

## Nortune's rising is one scene map and one battle

The original's Nortune stretch is: Fei's chair session 1 (map 618 #0: narration msg0, a
save prompt, `SetVar var[054] #11`, `SetVarBit var[248] #2`) → map 198 entrance 8 (A Block
gate at night: the party reset to Bart, camera flights over the district, narration
msg39–42, `SetCharacterGear #3 #18`, `BattleThenMap #8 ... #618 #0`) → session 2 (`SetAcc
#258` → map 273 #9). R2 cuts in after the bit is set and rejoins at 198 #8 with the
story back at 252, so the rising, the battle and the chair's bookkeeping stay the
original's. Rico is character 5, Bart 3; Sigmund's portrait is face 76 (model 2 on 237,
model 1 on 231/234); map 234 draws everyone at `SetScale #2500`.

## The Soylent facility is the game's own cut dungeon

The "stills" of chapter 57's Soylent stretch are not backgrounds: maps 621 (gate hall, 7
doorways), 620 (holding hall, 4 doorways, ten Wel sprites whose talk scripts show empty
messages msg4–msg11) and 622 (the tank room, the party's walk-in and the Sufal Mass's
breakout scripted) are walkable rooms the original only flies its camera over. R3 builds
its three rooms on them (`map N from K`), so no sprite needs borrowing and no art is made.
Map 622's entrance 1 is the original's own "fight now" entrance (the debug map's way in):
prep menu, `Battle #9`, then the scene the original plays after the fight.
