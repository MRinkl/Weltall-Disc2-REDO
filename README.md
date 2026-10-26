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
pack/   story documents → copy to <Weltall>/Weltall/Content/Story/disc2-redo/
docs/   design bible, map register, story-value register
```

## Status

Design. No pack files yet. The first playable sequence is R4 (Ramsus' assault on Nisan,
played as Elly); see the build order in the bible.

## Requirements

- Weltall 0.8.x built with `--expansion` (or a stock build if it loads extra packs from
  `Content/Story`; to be verified).
- Your own USA (or English undub) Xenogears disc images in Weltall's `Games` folder.

## Credits

Weltall by Roman215 (MIT). Xenogears © Square Enix. The Disc 2 script used as reference
is the GameFAQs transcript by Sheamon. Chapter titles and corrected line meanings from the
Xenogears/Xenosaga Study Guide. Fan discussion from r/XenoGears.
