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
| R3 Soylent | 57 (252–262) | TBD | |
| R2 Nortune | 57 (252–262) | TBD | |
| R1 Nisan defence | 57 (252–262) | TBD | |
| R5 Mahanon eve | 60 (285–287) | TBD | chair map 617 → `ChangeMap #303 #3` |
| R6 Mahanon | 61 (288–289) | TBD | narration map 619 |
| R7 Golgoda | 62 (290–294) | TBD | Shevat hangar scene is disc-2 map 164 (Renk et al.) |
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
