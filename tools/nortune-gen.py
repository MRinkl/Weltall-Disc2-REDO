import re, os
OUT = '/private/tmp/claude-501/-Users-mark-Documents-openbor-build/956de2c3-7cb3-4800-8cfb-71f048a61b2d/scratchpad/weltall/Content/Story/disc2/'

PARTY = """; The party: Fei, Bart, Rico.
""" + "".join(f"actor {i} script 0:\n    SetPartyCharacter #{i-1}\n    SetMessageFace #{i-1}\n{{SCALE}}    End\n" for i in range(1,12)) + \
"".join(f"actor {i} script 1:\n" for i in range(1,12)) + """    If Scene == #0 else Held
    PlayerControlStep
    End
Held:
    Stop
    End
"""

def finish(text, actors):
    """Append the 'does not do' section: every actor's scripts 0-3 not defined get End."""
    defined = set()
    for m in re.finditer(r'^actor (\d+) script (\d+):', text, re.M):
        defined.add((int(m.group(1)), int(m.group(2))))
    missing = [(a, s) for a in range(actors) for s in range(4) if (a, s) not in defined]
    tail = "\n; What an actor does not do.\n" + "".join(f"actor {a} script {s}:\n" for a, s in missing) + "    End\n"
    return text + tail

def check_widths(name, text):
    for m in re.finditer(r'^message (\w+)\n\{\n(.*?)\n\}', text, re.M | re.S):
        body = m.group(2).split('\n')
        speaker = body[0] if not body[0].startswith('"') else None
        lines = body[1:] if speaker else body
        pages = '\n'.join(lines).split('{page}')
        for p in pages:
            pl = p.split('\n')
            if len(pl) > 4:
                print(f"{name}/{m.group(1)}: {len(pl)} lines on a page")
            for l in pl:
                plain = re.sub(r'\{[^}]*\}', '', l).strip('"')
                if len(plain) > 26:
                    print(f"{name}/{m.group(1)}: {len(plain)} chars: {plain!r}")

docs = {}

# ---------------------------------------------------------------- 618 detour
docs['nortune-way-in.txt'] = """; Into Nortune, played. The original's first session in Fei's chair (map 618, entrance 0) tells of the Solaris
; Mobile Surface Supremacy Weapon and of going to Nortune, then goes to Nortune's A Block gate at night (map 198,
; entrance 8), where the Central District's rising is narrated over the gate and the Yggdrasil IV's battle with the
; Mobile Weapon is fought, and from there back to the chair's second session. The expanded second disc leaves the
; chair for the gate under curfew, a map of its own, with Fei, Bart and Rico and the story at the battleship's own
; value; the Kaiser's hall, the tactical command room and the bridge follow, and from the bridge the game goes on to
; the original's scene at the gate, the story at the original's value, where the rising and the battle are its own.
map 618
detour @0x0740 to Nortune ChangeMap #198 #8
Nortune:
    SetVar var[000] #254
    PartyAdd 3
    PartyAddWait
    PartyAdd 5
    PartyAddWait
    ChangeMap #745 #0
    StopAndHalt
"""

# ---------------------------------------------------------------- 745 the gate
gate = """; Nortune's A Block east gate under curfew, played: the map the original's narration of the rising plays over
; (map 198), on the night the party comes for the Central District, with the Imperial Guard holding the gate.
; Rico, the Battling Champion and the Kaiser's son, gets the party through.
map 745 from 198

message Halt
{
Imperial Guard
"Halt!{wait 0A} The capital is
under curfew.{page}No one passes this gate
tonight. Not with that
thing in the sky."
}

message Open
{
Rico
"Open it."
}

message Champ
{
Imperial Guard
"...The Champ!?{page}Y-yes, sir!{wait 0A} Open the gate!{page}...Sir, the Kaiser is
seeing no one tonight."
}

message SeeMe
{
Rico
"He'll see me."
}

message FirstName
{
Bart
"Big guy...{wait 0A} you're on
first-name terms with
the Kaiser of Kislev?"
}

message Father
{
Rico
"...He's my father.{page}Don't make a thing
of it."
}

message Mentioned
{
Bart
"Your father.{wait 0A} The Kaiser.{page}You might've mentioned
that back on the ship."
}

message Thanks
{
Fei
"Rico...{wait 0A} thanks."
}

message Watch
{
Imperial Guard
"Curfew.{wait 0A} Go home.{page}The sky over Aveh lit
up last night.{wait 0A} They say
it was Solaris."
}

message Post
{
Imperial Guard
"Every Gear in the
capital is up on the
walls.{page}And every man knows
it won't be enough."
}

actors 18
unsigned 00A-00E 016-01C 026-02A 030 036 1C0-1CC 1FC-224 240-250 400 41A-41C
entrances
; From the south of A Block, where the party comes in.
entrance x -142 z -731 layer 0 camera 0 facing 0
; A step before the gate (the tests' way in).
entrance x 395 z -182 layer 0 camera 0 facing 2

define Scene var[402]
actor 0 script 0:
    SetHiddenModel
    DisableTalk
    MusicLoad #58
    End

{PARTY}
; At the gate: the guard's scene begins when the party reaches it (a touch trigger has no DisableTalk).
actor 12 script 0:
    SetHiddenModel
    SetPosition #425 #-182
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 20 10 100 0
    SetCollisionFlags #1
    End
actor 12 script 3:
    If Scene == #0 else Begun
    SetVarTrue Scene
    StartScript actor13 script4@3
Begun:
    End

; The guard's scene (a script no actor runs by itself: script 1 would run at the map's start).
actor 13 script 0:
    SetHiddenModel
    DisableTalk
    End
actor 13 script 4:
    DisablePlayer
    Wait #20
    MessageAtActor actor14 Halt 0
    WaitMessageClosed
    Wait #20
    MessageAtActorPortrait actor6 Open 5
    WaitMessageClosed
    MessageAtActor actor14 Champ 0
    WaitMessageClosed
    MessageAtActorPortrait actor6 SeeMe 5
    WaitMessageClosed
    MessageAtActorPortrait actor4 FirstName 3
    WaitMessageClosed
    MessageAtActorPortrait actor6 Father 5
    WaitMessageClosed
    MessageAtActorPortrait actor4 Mentioned 3
    WaitMessageClosed
    MessageAtActorPortrait actor1 Thanks 0
    WaitMessageClosed
    Wait #20
    ScreenFade #1 #0 #0 #0 #30
    Wait #30
    ChangeMap #746 #0
    StopAndHalt

; The gate's guards, where the map has them.
actor 14 script 0:
    SetModel #0
    SetPosition #334 #-184
    SetFacingCode 3
    SetStateFlags 0 0x2000
    SetCollisionSize 40 40 150 0
    End
actor 14 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Halt 0
    WaitMessageClosed
    EnableControls
    End
actor 15 script 0:
    SetModel #5
    SetPosition #314 #-188
    SetFacingCode 3
    SetStateFlags 0 0x2000
    SetCollisionSize 20 20 150 0
    End
actor 15 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Post 0
    WaitMessageClosed
    EnableControls
    End

; The watch on the street.
actor 16 script 0:
    SetModel #0
    SetPosition #-19 #-207
    SetFacingCode 2
    SetStateFlags 0 0x2000
    SetCollisionSize 20 20 150 0
    End
actor 16 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Watch 0
    WaitMessageClosed
    EnableControls
    End
actor 17 script 0:
    SetModel #0
    SetPosition #-148 #-450
    SetFacingCode 0
    SetStateFlags 0 0x2000
    SetCollisionSize 20 20 150 0
    End
actor 17 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Post 0
    WaitMessageClosed
    EnableControls
    End
"""
docs['nortune-gate.txt'] = finish(gate.replace('{PARTY}', PARTY.replace('{SCALE}', '')), 18)

# ---------------------------------------------------------------- 746 the Kaiser's hall
hall = """; The Kaiser's hall in Nortune's Imperial Palace, played: the first disc's audience room (map 237), where Sigmund
; refuses the Fatima prince the Empire's heart and yields it to Kislev's own records, which Rico brings him.
; What the chair narrates ("Uncovering the truth from some ancient records, Bart activated the secret battleship")
; is said here. The south door leads to the tactical command room.
map 746 from 237

message AfterCurfew
{
Sigmund
"The Champ walks into my
hall after curfew...{page}with the Fatima boy and
the pilot from Lahan.{page}Say what you came
to say."
}

message Ship
{
Bart
"The Central District.{wait 0A}
It's a ship.{page}My ancestor Roni built
it after the great war
with Solaris.{page}That Mobile Weapon is a
day out from Nisan.{page}Your district is the one
thing on Ignas that can
stand up to it."
}

message FairyTale
{
Sigmund
"A fairy tale.{page}Five hundred years of
Kislev stand on that
ground.{page}I will not tear up my
capital on a pirate's
word.{wait 0A} Leave."
}

message NoKislev
{
Fei
"Kaiser.{wait 0A} When that thing
is done with Nisan...{page}there won't be a Kislev
left to stand on."
}

message Silence
{
Sigmund
"..."
}

message Archive
{
Rico
"Hammer kept people.{wait 0A}
They still talk to me.{page}The Battling Committee
has an archive under
D Block.{page}The founding charter
is in it.{page}Roni Fatima's name is
on the keel plate.{wait 0A}
I've seen it."
}

message BroughtToMe
{
Sigmund
"...The Committee's
archive.{page}You went down into the
dark for your Empire's
secret...{page}...and you brought it
to me."
}

message ToKislev
{
Rico
"I brought it to Kislev."
}

message Stations
{
Sigmund
"...Then Kislev will
hear it.{page}Below the tactical
command are the old
control stations.{page}Three of them, sealed
since my grandfather's
day.{page}Raise my city, Fatima.{wait 0A}
And pray you are right."
}

message CountOnIt
{
Bart
"Count on it."
}

message Go
{
Sigmund
"Three stations.{wait 0A}
Below the tactical
command.{page}Go."
}

message Lift
{
Associate
"The lift to the tactical
command is through the
south door, then down."
}

message InTheHall
{
Imperial Guard
"...!{page}The Champ.{wait 0A} In the
Kaiser's hall."
}

actors 25
unsigned 00A-00E 016-01A 026-02A 030 036 200-224
entrances
; From the gate, by the south door; the Kaiser's scene begins at once.
entrance x 262 z -152 layer 0 camera keep facing 0

define Scene var[402]
actor 0 script 0:
    SetHiddenModel
    DisableTalk
    MusicLoad #47
    End

{PARTY}
; The Kaiser's scene, as the party comes in.
actor 12 script 0:
    SetHiddenModel
    DisableTalk
    SetVarTrue Scene
    End
actor 12 script 1:
    DisablePlayer
    Wait #40
    MessageAtActorPortrait actor14 AfterCurfew 76
    WaitMessageClosed
    MessageAtActorPortrait actor4 Ship 3
    WaitMessageClosed
    MessageAtActorPortrait actor14 FairyTale 76
    WaitMessageClosed
    MessageAtActorPortrait actor1 NoKislev 0
    WaitMessageClosed
    Wait #30
    MessageAtActorPortrait actor14 Silence 76
    WaitMessageClosed
    MessageAtActorPortrait actor6 Archive 5
    WaitMessageClosed
    Wait #30
    MessageAtActorPortrait actor14 BroughtToMe 76
    WaitMessageClosed
    MessageAtActorPortrait actor6 ToKislev 5
    WaitMessageClosed
    Wait #40
    MessageAtActorPortrait actor14 Stations 76
    WaitMessageClosed
    MessageAtActorPortrait actor4 CountOnIt 3
    WaitMessageClosed
    SetVarFalse Scene
    EnablePlayer
    End

; The south door, to the tactical command room.
actor 13 script 0:
    SetHiddenModel
    SetPosition #262 #-210
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 40 10 10 0
    SetCollisionFlags #1
    End
actor 13 script 3:
    ChangeMap #747 #0
    StopAndHalt

; Kaiser Sigmund, where the audience room has him.
actor 14 script 0:
    SetModel #2
    SetPositionXYZ #-190 #0 #-10
    SetFacingCode 6
    SetMessageFace #76
    End
actor 14 script 2:
    DisableControls
    FaceActor party0
    MessageAtActorPortrait self Go 76
    WaitMessageClosed
    EnableControls
    End

; The guard at the hall's side.
actor 19 script 0:
    SetModel #1
    SetPosition #156 #125
    SetFacingCode 4
    End
actor 19 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self InTheHall 0
    WaitMessageClosed
    EnableControls
    End

; The Kaiser's associate.
actor 24 script 0:
    SetModel #4
    SetPosition #-112 #-150
    SetFacingCode 0
    End
actor 24 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Lift 0
    WaitMessageClosed
    EnableControls
    End
"""
docs['nortune-audience.txt'] = finish(hall.replace('{PARTY}', PARTY.replace('{SCALE}', '')), 25)

# ---------------------------------------------------------------- 747 the tactical command room
command = """; The Central District's tactical command room, played: the first disc's map of it (map 231), with the three
; control stations the Kaiser unsealed, which raise the district in any order, and the lift to the bridge, which
; runs once all three are set. The puzzle the chair narrates past ("Bart activated the secret battleship").
map 747 from 231

message Keel
{
Bart
"Keel clamps.{wait 0A} Five
hundred years of rust...{page}...and she still
answers."
}

message Engines
{
Bart
"Lift engines.{page}Roni, you crazy
old man."
}

message Link
{
Bart
"Bridge link.{wait 0A} The
Yggdrasil's handshake is
in the keel's code.{page}The 'Sand Cruiser' was
always the heart of her."
}

message One
{
Bart
"That's one."
}

message Two
{
Bart
"Two."
}

message AllThree
{
Rico
"That's all three.{page}Feel that?{wait 0A} The whole
floor's humming."
}

message LiftLive
{
Bart
"The lift's live.{page}Bridge.{wait 0A} Now."
}

message Dead
{
Fei
"The lift's dead.{page}The district's power
is still down."
}

message Sealed
{
Kislev Soldier
"The Kaiser's order came
down an hour ago.{page}Doors nobody's opened
in a hundred years...{page}They opened."
}

message Hum
{
Kislev Soldier
"You feel that?{wait 0A} Under
the floor.{page}...The District's never
made that sound."
}

actors 19
unsigned 00A-00E 026-02A 030 036 200-224
entrances
; From the Kaiser's hall, by the south door.
entrance x -84 z -291 layer 0 camera keep facing 0
; A step before each station (the tests' way in).
entrance x -440 z -55 layer 0 camera keep facing 4
entrance x -160 z -55 layer 0 camera keep facing 2
entrance x 1240 z -155 layer 0 camera keep facing 4
; A step before the lift's way in with the three stations set (the tests' way in).
entrance x 397 z -60 layer 0 camera keep facing 4

define Scene var[402]
define Count var[404]
define KeelSet var[406]
define EnginesSet var[408]
define LinkSet var[40A]
actor 0 script 0:
    SetHiddenModel
    DisableTalk
    MusicLoad #71
    End

{PARTY}
; The keel station (a touch trigger has no DisableTalk).
actor 12 script 0:
    SetHiddenModel
    SetPosition #-500 #-55
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 30 10 30 0
    SetCollisionFlags #1
    End
actor 12 script 3:
    If KeelSet == #0 else KeelDone
    SetVarTrue KeelSet
    DisablePlayer
    MessageAtActorPortrait actor4 Keel 3
    WaitMessageClosed
    StartScriptWaitEnd actor15 script4@3
    EnablePlayer
KeelDone:
    End

; The lift engines' station.
actor 13 script 0:
    SetHiddenModel
    SetPosition #-100 #-55
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 30 10 30 0
    SetCollisionFlags #1
    End
actor 13 script 3:
    If EnginesSet == #0 else EnginesDone
    SetVarTrue EnginesSet
    DisablePlayer
    MessageAtActorPortrait actor4 Engines 3
    WaitMessageClosed
    StartScriptWaitEnd actor15 script4@3
    EnablePlayer
EnginesDone:
    End

; The bridge link's station.
actor 14 script 0:
    SetHiddenModel
    SetPosition #1300 #-155
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 30 10 30 0
    SetCollisionFlags #1
    End
actor 14 script 3:
    If LinkSet == #0 else LinkDone
    SetVarTrue LinkSet
    DisablePlayer
    MessageAtActorPortrait actor4 Link 3
    WaitMessageClosed
    StartScriptWaitEnd actor15 script4@3
    EnablePlayer
LinkDone:
    End

; The count of stations set, and what is said at each (a script no actor runs by itself).
actor 15 script 0:
    SetHiddenModel
    DisableTalk
    End
actor 15 script 4:
    AddVar Count #1
    If Count == #1 else NotOne
    MessageAtActorPortrait actor4 One 3
    WaitMessageClosed
    End
NotOne:
    If Count == #2 else NotTwo
    MessageAtActorPortrait actor4 Two 3
    WaitMessageClosed
    End
NotTwo:
    MessageAtActorPortrait actor6 AllThree 5
    WaitMessageClosed
    MessageAtActorPortrait actor4 LiftLive 3
    WaitMessageClosed
    End

; The lift to the bridge.
actor 16 script 0:
    SetHiddenModel
    SetPosition #397 #45
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 40 10 30 0
    SetCollisionFlags #1
    End
actor 16 script 3:
    If Count == #3 else Down
    ChangeMap #748 #0
    StopAndHalt
Down:
    DisablePlayer
    MessageAtActorPortrait actor1 Dead 0
    WaitMessageClosed
    WalkLeaderTo #397 #-40
    EnablePlayer
    End

; The soldier on watch.
actor 17 script 0:
    SetModel #2
    SetPosition #-213 #33
    SetFacingCode 1
    End
actor 17 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Sealed 0
    WaitMessageClosed
    EnableControls
    End

; Before the lift with the three stations set: the tests' way in, which takes the lift at once.
actor 18 script 0:
    SetHiddenModel
    SetPosition #397 #-120
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 40 10 30 0
    SetCollisionFlags #1
    End
actor 18 script 3:
    SetVar Count #3
    StartScriptWaitEnd actor16 script3@3
    End
"""
docs['nortune-command.txt'] = finish(command.replace('{PARTY}', PARTY.replace('{SCALE}', '')), 19)

# ---------------------------------------------------------------- 748 the bridge
bridge = """; The Central District's bridge, played: the first disc's map of the Kaiser's bridge (map 234), where Sigmund
; acknowledges his son before his officers and gives the ship to its new master. What the chair narrates
; ("Commanded by its 'new master', the secret battleship stood before the Mobile Weapon") begins here, and the
; game goes on to the original's scene at the gate (map 198, entrance 8): the rising, and the battle.
map 748 from 234

message HearMe
{
Sigmund
"Officers of Kislev.{wait 0A}
Hear me.{page}The man beside the
Fatima prince is
Ricardo Banderas.{page}The Battling Champion.{wait 1E}{page}My son."
}

message Gasp
{
Officer
"...!"
}

message Denied
{
Sigmund
"I denied him for the
throne's sake.{page}Tonight the throne is a
ship's deck.{wait 0A} I am done
denying.{page}Whatever comes down on
us out of that sky...{page}he stands where I stand."
}

message OldMan
{
Rico
"...Old man.{page}...Don't make me say
anything."
}

message RicoDots
{
Fei
"Rico..."
}

message WakeHer
{
Bart
"Alright!{wait 0A} Yggdrasil's
locked into the keel.{page}Sigurd, Maison, all
hands to stations.{page}Kaiser...{wait 0A} with your
permission.{page}Let's wake her up."
}

message Yours
{
Sigmund
"She is yours, Fatima.{page}Raise her."
}

actors 25
unsigned 00A-00E 026-02A 030 036 200-224
entrances
; From the lift; the Kaiser's scene begins at once.
entrance x -638 z 1504 layer 0 camera keep facing 2

define Scene var[402]
actor 0 script 0:
    SetHiddenModel
    DisableTalk
    MusicLoad #21
    SkyboxParams 0x0 0x0 0x140 0x0 0x0 0x0 0x0
    SkyboxHorizon #0 #4000 #-1024
    SkyboxColors #40 #50 #180 #40 #50 #180 #150 #168 #144 #0 #0 #0
    End

{PARTY}
; The Kaiser's scene, as the party comes onto the bridge.
actor 12 script 0:
    SetHiddenModel
    DisableTalk
    SetVarTrue Scene
    End
actor 12 script 1:
    DisablePlayer
    Wait #40
    MessageAtActorPortrait actor24 HearMe 76
    WaitMessageClosed
    MessageAtActor actor22 Gasp 0
    WaitMessageClosed
    MessageAtActorPortrait actor24 Denied 76
    WaitMessageClosed
    Wait #30
    MessageAtActorPortrait actor6 OldMan 5
    WaitMessageClosed
    MessageAtActorPortrait actor1 RicoDots 0
    WaitMessageClosed
    MessageAtActorPortrait actor4 WakeHer 3
    WaitMessageClosed
    MessageAtActorPortrait actor24 Yours 76
    WaitMessageClosed
    Wait #30
    ScreenFade #1 #0 #0 #0 #30
    Wait #30
    PartyRemove 3
    PartyRemove 5
    SetVar var[000] #252
    ChangeMap #198 #8
    StopAndHalt

; What the bridge looks out on: the dock's ship and Gears, as the map has them.
actor 16 script 0:
    SetGearModel #62
    SetScale #6000
    SetPositionXYZ #10000 #1510 #690
    SetModelTurnSpeed #2047
    End
actor 17 script 0:
    SetGearModel #8
    SetScale #2048
    SetPositionXYZ #1800 #1900 #720
    End
actor 18 script 0:
    SetGearModel #8
    SetScale #2048
    SetPositionXYZ #1800 #1100 #720
    End

; The officers at their stations.
actor 19 script 0:
    SetModel #3
    SetPosition #-39 #1422
    SetScale #2500
    SetFacingCode 3
    End
actor 20 script 0:
    SetModel #3
    SetPosition #-39 #1608
    SetScale #2500
    SetFacingCode 3
    End
actor 21 script 0:
    SetModel #3
    SetPosition #120 #1300
    SetScale #2500
    SetFacingCode 3
    End
actor 22 script 0:
    SetModel #4
    SetPosition #-300 #1554
    SetScale #2500
    SetFacingCode 3
    End
actor 23 script 0:
    SetModel #3
    SetPosition #-94 #1610
    SetScale #2500
    SetFacingCode 1
    End

; Kaiser Sigmund, where the bridge has him.
actor 24 script 0:
    SetModel #1
    SetPosition #-144 #1116
    SetScale #2500
    SetMessageFace #76
    SetFacingCode 3
    End
"""
docs['nortune-bridge.txt'] = finish(bridge.replace('{PARTY}', PARTY.replace('{SCALE}', '    SetScale #2500\n')), 25)

for name, text in docs.items():
    check_widths(name, text)
    open(OUT + name, 'w').write(text)
    print(name, len(text.splitlines()), 'lines')
