import re
OUT = '/private/tmp/claude-501/-Users-mark-Documents-openbor-build/956de2c3-7cb3-4800-8cfb-71f048a61b2d/scratchpad/weltall/Content/Story/disc2/'

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

party = "".join(f"actor {i} script 0:\n    SetPartyCharacter #{i-1}\n    SetMessageFace #{i-1}\n    End\n" for i in range(1, 12))
party += "".join(f"actor {i} script 1:\n" for i in range(1, 12)) + """    If Scene == #0 else Held
    PlayerControlStep
    End
Held:
    Stop
    End
"""

docs = {}

docs['night-before-way-in.txt'] = """; The night before Mahanon, played. The chair's fourth session (map 617, entrance 4), the second time through, tells
; in three pages what the scouts found (Solaris's whole force on Mahanon, the Solarians turned to weapons, the
; Ministry at their head) and of the decision to go at dawn, then gives Fei and Elly to the deck of the Yggdrasil
; (map 303, entrance 3), where the night's scenes play. The expanded second disc passes over the pages and goes,
; with the same party, to the Yggdrasil's bridge, a map of its own, where that is said, and from the bridge to the
; same deck with the story back at the original's value.
map 617
detour @0x0904 to Told StartScriptWaitEnd actor31 script14@1
Told:
    Jump @0x0907
detour @0x092D to Bridge ChangeMap #303 #3
Bridge:
    SetVar var[000] #286
    ChangeMap #752 #0
    StopAndHalt
"""

bridge = """; The Yggdrasil's bridge on the night before Mahanon, played: the ship's bridge (map 290) with Sigurd, Bart and
; Citan at the chart, where what the chair's pages tell is said: the scouts' word of the force on Mahanon, what
; the Solarians have become, and that the ship goes at dawn with everything there is. Fei goes from here to the
; deck, where the original's night plays: Elly told to stay, the crew's teasing, her door.
map 752 from 290

message Scouts
{
Sigurd
"The scouts are back from
the north.{page}Solaris sits on Mahanon.{wait 0A}
All of it."
}

message WhatIsLeft
{
Citan
"What is left of it.{page}Not a nation.{wait 0A} Not Gebler.{page}The Gaetia Key turned
nearly every Solarian
into a weapon.{page}The Ministry commands
them now."
}

message NothingBetween
{
Bart
"So it's the Ministry,
god's wisdom, and
nothing in between.{page}Then we go.{wait 0A} All of us.{wait 0A}
Everything we've got."
}

message NoWayBack
{
Sigurd
"Nisan's militia, Shevat's
Gears, the Yggdrasil.{page}It will not be enough to
promise anyone a way
back, young master."
}

message Dawn
{
Bart
"I know.{page}We launch at dawn."
}

message AtDawn
{
Fei
"At dawn."
}

message Tonight
{
Citan
"Fei.{wait 0A} Whoever should not
be aboard tomorrow...{page}tell them tonight.{wait 0A}
Not at the ramp."
}

message IKnowWho
{
Fei
"...I know who."
}

message Sleep
{
Sigurd
"Get some sleep, Fei.{page}Dawn comes whether we
are ready or not."
}

message Straight
{
Bart
"Say it to her straight.{page}...Not that I'd know
how."
}

message Counted
{
Citan
"The scouts counted the
Gears on the hull twice.{page}They stopped at a
thousand."
}

message Course
{
Crewman
"Course laid in for
Mahanon, sir.{page}Whatever that means
for us."
}

message Letter
{
Crewman
"I wrote my mother
tonight.{page}Didn't say where."
}

actors 19
unsigned 00A-00E 026-02A 030 036 100-12E 180-190 1C0-1CC 1FC-1FE 2C0-2DE
entrances
; The bridge's door, where Fei and Elly come in.
entrance x 0 z 640 layer 0 camera keep facing 4
; A step before the chart (the tests' way in).
entrance x 0 z 210 layer 0 camera keep facing 4

define Scene var[402]
define Briefed var[404]
actor 0 script 0:
    SetHiddenModel
    DisableTalk
    CameraSet #0 #22 #512
    End

; The party: Fei and Elly, as the chair leaves it.
{PARTY}
; Sigurd at the chart, Bart and Citan with him, where the bridge has them.
actor 12 script 0:
    SetModel #10
    SetMessageFace #27
    SetPosition #-8 #8
    SetFacingCode 0
    End
actor 12 script 2:
    DisableControls
    FaceActor party0
    MessageAtActorPortrait self Sleep 27
    WaitMessageClosed
    EnableControls
    End
actor 13 script 0:
    SetModel #7
    SetMessageFace #3
    SetPosition #57 #127
    SetFacingCode 2
    End
actor 13 script 2:
    DisableControls
    FaceActor party0
    MessageAtActorPortrait self Straight 3
    WaitMessageClosed
    EnableControls
    End
actor 14 script 0:
    SetModel #11
    SetMessageFace #2
    SetPosition #-82 #204
    SetFacingCode 6
    End
actor 14 script 2:
    DisableControls
    FaceActor party0
    MessageAtActorPortrait self Counted 2
    WaitMessageClosed
    EnableControls
    End

; The crew at the helm.
actor 15 script 0:
    SetModel #0
    SetPosition #-88 #-280
    SetFacingCode 4
    End
actor 15 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Course 0
    WaitMessageClosed
    EnableControls
    End
actor 16 script 0:
    SetModel #0
    SetPosition #20 #-280
    SetFacingCode 4
    End
actor 16 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Letter 0
    WaitMessageClosed
    EnableControls
    End

; At the chart, Sigurd, Bart and Citan in view: the briefing, when Fei reaches it, once (a party standing in the
; trigger touches it again as soon as the scene ends).
actor 17 script 0:
    SetHiddenModel
    SetPosition #0 #150
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 250 10 20 0
    SetCollisionFlags #1
    End
actor 17 script 3:
    If Briefed == #0 else Begun
    SetVarTrue Briefed
    SetVarTrue Scene
    DisablePlayer
    Wait #20
    MessageAtActorPortrait actor12 Scouts 27
    WaitMessageClosed
    MessageAtActorPortrait actor14 WhatIsLeft 2
    WaitMessageClosed
    MessageAtActorPortrait actor13 NothingBetween 3
    WaitMessageClosed
    MessageAtActorPortrait actor12 NoWayBack 27
    WaitMessageClosed
    MessageAtActorPortrait actor13 Dawn 3
    WaitMessageClosed
    Wait #20
    MessageAtActorPortrait actor1 AtDawn 0
    WaitMessageClosed
    MessageAtActorPortrait actor14 Tonight 2
    WaitMessageClosed
    Wait #30
    MessageAtActorPortrait actor1 IKnowWho 0
    WaitMessageClosed
    SetVarFalse Scene
    EnablePlayer
Begun:
    End

; The door, to the deck and the original's night.
actor 18 script 0:
    SetHiddenModel
    SetPosition #0 #700
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 60 10 20 0
    SetCollisionFlags #1
    End
actor 18 script 3:
    DisablePlayer
    ScreenFade #1 #0 #0 #0 #30
    Wait #30
    SetVar var[000] #285
    ChangeMap #303 #3
    StopAndHalt
"""
docs['night-before-bridge.txt'] = finish(bridge.replace('{PARTY}', party), 19)

for name, text in docs.items():
    check_widths(name, text)
    open(OUT + name, 'w').write(text)
    print(name, len(text.splitlines()), 'lines')
