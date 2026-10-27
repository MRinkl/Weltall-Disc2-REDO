import re
OUT = '/private/tmp/claude-501/-Users-mark-Documents-openbor-build/956de2c3-7cb3-4800-8cfb-71f048a61b2d/scratchpad/weltall/Content/Story/disc2/'

def party(slots):
    """Party actors: (actor, character) pairs; script 1 walks unless the scene holds them."""
    text = "".join(f"actor {a} script 0:\n    SetPartyCharacter #{c}\n    SetMessageFace #{c}\n    End\n" for a, c in slots)
    text += "".join(f"actor {a} script 1:\n" for a, c in slots) + """    If Scene == #0 else Held
    PlayerControlStep
    End
Held:
    Stop
    End
"""
    return text

def finish(text, actors):
    defined = set()
    for m in re.finditer(r'^actor (\d+) script (\d+):', text, re.M):
        defined.add((int(m.group(1)), int(m.group(2))))
    missing = [(a, s) for a in range(actors) for s in range(4) if (a, s) not in defined]
    return text + "\n; What an actor does not do.\n" + "".join(f"actor {a} script {s}:\n" for a, s in missing) + "    End\n"

def check_widths(name, text):
    for m in re.finditer(r'^message (\w+)\n\{\n(.*?)\n\}', text, re.M | re.S):
        body = m.group(2).split('\n')
        speaker = body[0] if not body[0].startswith('"') else None
        lines = body[1:] if speaker else body
        for p in '\n'.join(lines).split('{page}'):
            pl = p.split('\n')
            if len(pl) > 4:
                print(f"{name}/{m.group(1)}: {len(pl)} lines on a page")
            for l in pl:
                plain = re.sub(r'\{[^}]*\}', '', l).strip('"')
                if len(plain) > 26:
                    print(f"{name}/{m.group(1)}: {len(plain)} chars: {plain!r}")

docs = {}

docs['mahanon-way-in.txt'] = """; Into Mahanon's wreck, played. The original goes from the continent's approach (map 652, the Yggdrasil at the hull,
; the narration of what Mahanon is) to the inside of the wreck as a camera's flight (map 653, three pages of narration
; and the save prompt), and on to the hallway the party walks to the rotting nucleus (map 654). The expanded second
; disc goes from the approach to the wreck's hull, a map of its own on map 653's floor, with the story at the wreck's
; own value, and from its far end to the same hallway, the story back at the original's value.
map 652
detour @0x0108 to Wreck ChangeMap #653 #0
Wreck:
    SetVar var[000] #289
    ChangeMap #749 #0
    StopAndHalt
"""

wreck = """; Inside Mahanon's wreck, played: the floor the original's camera flies over (map 653), walked from the hull's
; breach up the great hall and around the ring, with what the narration says of the ship ("It was determined, by
; examining the inside of the wreckage...") read from the ship's own log where it says it, in the disc's words.
; The way on, past the ring, is the hallway to the depths (map 654), the original's own, entered as the flight enters it.
map 749 from 653

message Log from map 653 message 0
message Passengers from map 653 message 1
message Onward from map 653 message 2

message Terminal
{
Citan
"A log terminal.{wait 0A} Still
powered, after all
this time..."
}

message Waiting
{
Fei
"Ten thousand years...{page}And it's still waiting
for someone to read it."
}

message Falls
{
Bart
"A ship this size
doesn't crash.{wait 0A} It falls.{page}Something inside her
went wrong first."
}

message Ribs
{
Citan
"Look at the hull's ribs.{page}They were grown,
not built.{page}Whoever sailed her
was not from here."
}

message WhatWeAre
{
Fei
"...Then that's what
we are.{page}What's left of
the passengers."
}

message Deeper
{
Bart
"The scanner says the
floor goes on under us.{page}A long way under."
}

actors 5
unsigned 00A-00E 026-02A 030 036 0C0-0CC
entrances
; The breach in the hull, where the original's camera starts.
entrance x 1324 z -2400 layer 0 camera keep facing 6
; A step before the log terminal (the tests' way in).
entrance x 0 z -1560 layer 0 camera keep facing 0
; A step before the ring (the tests' way in).
entrance x 0 z -450 layer 0 camera keep facing 0
; A step before the way down (the tests' way in).
entrance x 0 z 770 layer 0 camera keep facing 0

define Scene var[402]
define Stage var[404]
actor 0 script 0:
    SetHiddenModel
    CameraSet #255 #20 #768
    SetCameraLockMask #199
    DisableTalk
    SetVar var[054] #2
    End

; The party: Fei, Citan, Bart, as the approach leaves it (map 653 gives it these three actors).
{PARTY}
; One trigger for the three stops, moved on from each: the log terminal, the ring, the way down. Entered at a
; later stop's entrance, it waits there.
actor 4 script 0:
    SetHiddenModel
    SetPosition #0 #-1500
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 250 10 20 0
    SetCollisionFlags #1
    If var[002] == #2 else NotRing
    SetVar Stage #1
    SetPosition #0 #-383
    End
NotRing:
    If var[002] == #3 else NotDown
    SetVar Stage #2
    SetPosition #0 #830
NotDown:
    End
actor 4 script 3:
    If Stage == #0 else NotLog
    SetVar Stage #1
    DisablePlayer
    MessageAtActorPortrait actor2 Terminal 9
    WaitMessageClosed
    SetWindowLayoutVar #30 #20 #0 #0 #321
    MessageCentered Log 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    MessageAtActorPortrait actor1 Waiting 0
    WaitMessageClosed
    MessageAtActorPortrait actor3 Falls 3
    WaitMessageClosed
    SetPosition #0 #-383
    EnablePlayer
    End
NotLog:
    If Stage == #1 else Down
    SetVar Stage #2
    DisablePlayer
    MessageAtActorPortrait actor2 Ribs 9
    WaitMessageClosed
    SetWindowLayoutVar #30 #70 #0 #0 #321
    MessageCentered Passengers 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    MessageAtActorPortrait actor1 WhatWeAre 0
    WaitMessageClosed
    MessageAtActorPortrait actor3 Deeper 3
    WaitMessageClosed
    SetPosition #0 #830
    EnablePlayer
    End
Down:
    DisablePlayer
    SetWindowLayoutVar #30 #80 #0 #0 #321
    MessageCentered Onward 83
    WaitMessageClosed
    SetCharacterLocked 0 #0
    SetCharacterLocked 0 #1
    SetVar var[000] #288
    ChangeMapTransition #17038 #0 #0 #32
    StopAndHalt
"""
docs['mahanon-wreck.txt'] = finish(wreck.replace('{PARTY}', party([(1, 0), (2, 9), (3, 3)])), 5)

docs['mahanon-cavern-way-in.txt'] = """; From the depths to Razael's cavern, played. The original's hallway (map 654) goes, after the rotting nucleus, to the
; cavern's scene (map 655): the camera's descent, the narration of the cavern and the Tree, the data, Krelian and
; Grahf. The expanded second disc goes to the cavern's floor first, a map of its own, with the story at the Tree's
; own value, and from there into the same scene past the narration the walk has said.
map 654
detour @0x5019 to Cavern ChangeMap #655 #0
Cavern:
    SetVar var[000] #291
    ChangeMap #750 #0
    StopAndHalt
"""

cavern = """; Razael's cavern, played: the floor of the original's scene (map 655), walked from the cavern's edge toward the two
; lights at its centre, with what the narration says of the cavern and the Tree ("We came to an enormous cavern...")
; said on the way, in the disc's words. At the centre the original's scene begins, past those pages.
map 750 from 655

message Cavern from map 655 message 6
message Glow from map 655 message 7
message Tree from map 655 message 8

message Swallow
{
Bart
"Big enough to swallow
Bledavik whole...{page}and Nortune after it."
}

message Lights
{
Citan
"There.{wait 0A} In the centre.{page}Two lights.{wait 0A} That is what
the Ministry has been
digging for."
}

message Beautiful
{
Fei
"Razael's Tree.{page}...It's beautiful.{wait 0A}
Why does that scare me?"
}

actors 31
unsigned 00A-00E 026-02A 030 036 0C0-0CC
entrances
; The cavern's edge, far from the lights.
entrance x 0 z -4500 layer 0 camera keep facing 0
; A step before the centre (the tests' way in).
entrance x 0 z -1360 layer 0 camera keep facing 0

define Scene var[402]
actor 0 script 0:
    SetHiddenModel
    CameraSet #255 #20 #384
    CameraZoom #5120 0
    DisableTalk
    MusicLoad #56
    End

; The party, whoever the depths leave in it.
{PARTY}
; The centre: the narration's pages, then the original's scene.
actor 12 script 0:
    SetHiddenModel
    SetPosition #0 #-1300
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 250 10 20 0
    SetCollisionFlags #1
    End
actor 12 script 3:
    If Scene == #0 else Begun
    SetVarTrue Scene
    DisablePlayer
    SetWindowLayoutVar #30 #70 #0 #0 #321
    MessageCentered Cavern 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    MessageAtActorPortrait actor4 Swallow 3
    WaitMessageClosed
    SetWindowLayoutVar #30 #70 #0 #0 #321
    MessageCentered Glow 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    MessageAtActorPortrait actor10 Lights 9
    WaitMessageClosed
    SetWindowLayoutVar #30 #70 #0 #0 #321
    MessageCentered Tree 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    MessageAtActorPortrait actor1 Beautiful 0
    WaitMessageClosed
    Wait #20
    ScreenFade #1 #255 #255 #255 #30
    Wait #30
    SetVar var[000] #291
    ChangeMap #655 #0
    StopAndHalt
Begun:
    End

; The scene's own actors, not here: the cavern is empty until the scene.
""" + "".join(f"actor {a} script 0:\n    RemoveActor self\n    End\n" for a in range(13, 31))
docs['mahanon-cavern.txt'] = finish(cavern.replace('{PARTY}', party([(i, i - 1) for i in range(1, 12)])), 31)

docs['mahanon-cavern-scene.txt'] = """; Razael's cavern's scene (map 655), entered from the cavern's floor in the expanded second disc: the pages the walk
; has said (the cavern, the two lights, the Tree) are passed over, and the story goes back to the original's value;
; the camera's descent, the data, Krelian and Grahf are the original's. Entered any other way, the scene is whole.
map 655
detour @0x074B to Said Message msg6 0
Said:
    If var[000] == #291 else Tell
    SetVar var[000] #290
    Jump @0x0760
Tell:
    Message msg6 0
    Jump @0x074F
"""

for name, text in docs.items():
    check_widths(name, text)
    open(OUT + name, 'w').write(text)
    print(name, len(text.splitlines()), 'lines')
