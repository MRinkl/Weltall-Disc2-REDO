# Weltall Disc 2 REDO

A playable second disc for Xenogears, as a story pack for
[Weltall](https://github.com/Roman215/Weltall) (the Unreal Engine 5 port), for Windows and
Linux.

The original Disc 2 narrates most of its second half from two chairs in a dark room.
This pack turns each narrated stretch into a played one: maps, NPCs, triggers, the boss
fights the disc already contains, and the original cutscenes in their original places.
Canon, lore, graphics and mechanics stay the game's own; nothing new is imported, because
Weltall cannot import models or movies. Every sequence branches from the original story
and rejoins it with identical saved state, so saves stay compatible with the unexpanded
game.

Start with [docs/DESIGN-BIBLE.md](docs/DESIGN-BIBLE.md): principles, sources, the
beat-by-beat map of the original disc, the eleven sequences of the redo (R1–R11), the
loose ends each closes, the two twists, the file layout and the build order.

## Layout

```
pack/   story documents → copy into <Weltall>/Weltall/Content/Story/disc2/ (Weltall gates only that folder on "Extended")
tests/  the Catch2 tests that play each sequence against the original, for Weltall's Tests/WeltallCore/Story/
engine/ the Weltall source changes the pack needs (also in the upstream PR): sprite slots from other maps
docs/   design bible, map register, story-value register
```

## Status

R4 (Ramsus' assault on Nisan, played as Elly) is written and under test: three documents,
a branch in the chair map, two maps of their own on Nisan's town and cathedral front, and a
test that plays it against the original session. See the build order in the bible.

## Requirements

- Weltall 0.8.x built with `--expansion` (or a stock build if it loads extra packs from
  `Content/Story`; to be verified).
- Your own USA (or English undub) Xenogears disc images in Weltall's `Games` folder.
- Optional: Perfect Works Build 0.11.4 unpacked into `Mods/PerfectWorks` (so that
  `Mods/PerfectWorks/gamefiles` exists). With its Script on, every line this pack quotes
  from the disc (`message X from map M message K`) is the mod's retranslation. Pre-patched
  Perfect Works discs are not read by Weltall; only the mod's release archive is.

## Credits

Weltall by Roman215 (MIT). Xenogears © Square Enix. The Disc 2 script used as reference
is the GameFAQs transcript by Sheamon. Chapter titles and corrected line meanings from the
Xenogears/Xenosaga Study Guide. Fan discussion from r/XenoGears.
