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

docs = {}

docs['golgoda-way-in.txt'] = """; Elly's leaving for Golgoda, played. The chair's fifth session (map 617, entrance 5) tells of her climb to Shevat and
; Krelian's call in two pages, then plays her unit's farewell in the hangar over stills (actor 31's script 15), then
; shows the hangar itself as a camera's flight (map 657) and goes to the chair session that plays Golgoda (map 619,
; entrance 3: Krelian's offer, the battle). The expanded second disc leaves the chair before the stills for the
; hangar's floor, a map of its own, with Elly alone and the story at her decision's value, and from there goes to
; the same Golgoda session with the story back at the original's value.
map 617
detour @0x099A to Hangar SetVar var[400] #1
Hangar:
    SetVar var[000] #292
    ChangeMap #751 #0
    StopAndHalt
"""

# The party: actor N + 1 is character N.
PARTY_SLOTS = [(i, i - 1) for i in range(1, 12)]
party = "".join(f"actor {a} script 0:\n    SetPartyCharacter #{c}\n    SetMessageFace #{c}\n    End\n" for a, c in PARTY_SLOTS)
party += "".join(f"actor {a} script 1:\n" for a, c in PARTY_SLOTS) + """    If Scene == #0 else Held
    PlayerControlStep
    End
Held:
    Stop
    End
"""

# The unit, where the hangar's flight has its people: who is which sprite is the hangar's guess; the faces are the chair's.
UNIT = [  # actor, model, x, z, facing, name, face, idle line (map 164's uniforms, where it stands its soldiers)
    (12, 2, 844, -240, 6, 'Renk', 65, 'RenkIdle'),
    (13, 2, 785, -274, 6, 'Helmholz', 69, 'HelmholzIdle'),
    (14, 2, 684, -266, 6, 'Stratski', 67, 'StratskiIdle'),
    (15, 2, 910, -140, 6, 'Vance', 68, 'VanceIdle'),
    (16, 2, 733, -251, 6, 'Broyer', 66, 'BroyerIdle'),
]

hangar = """; Shevat's hangar on the night Elly leaves for Golgoda, played: the hangar map that has her unit's own sprites (map
; 164, the hangar the story brings her unit to), with them waiting by the last Omnigear. The chair's pages of her
; climb and Krelian's call are read at her arrival and its page of her departure at the end, from the disc; her
; unit's farewell is the chair's own scene (map 617's messages 60 to 84), spoken where they stand. From the Omnigear the game goes to Golgoda, the
; chair's session that plays it (map 619, entrance 3), the story at the original's value.
map 751 from 164

""" + "".join(f"message Line{n} from map 617 message {n}\n" for n in range(60, 85)) + """
message Ascend from map 617 message 58
message Depart from map 617 message 59

message RenkIdle
{
Renk
"...Say it again, that
you're going alone.{page}No.{wait 0A} Don't."
}

message HelmholzIdle
{
Helmholz
"Her weapons are loaded.{wait 0A}
All of them.{page}I did it myself.{wait 0A}
Three times."
}

message StratskiIdle
{
Stratski
"Golgoda.{wait 0A} It's a hill.{page}Just a hill. Why does
the name feel like that?"
}

message VanceIdle
{
Vance
"We ran from Solaris with
you. We'd fly into it
with you.{page}...If you'd let us."
}

message BroyerIdle
{
Broyer
"The others are asleep
in Nisan.{page}Don't wake them.{wait 0A}
They'd only try
to stop you."
}

message Mechanic
{
Shevat Mechanic
"She's fuelled and the
seals are checked.{page}The last Omnigear
in Shevat.{wait 0A} Bring
her back."
}

message Watchman
{
Shevat Mechanic
"They've been standing
there since the call
came in.{page}Nobody told them to."
}

actors 21
unsigned 00A-00E 026-02A 030 036 080-0BE 402-40A
entrances
; The hangar's west end, where Elly comes in.
entrance x -1031 z -268 layer 0 camera keep facing 2
; A step before her unit (the tests' way in).
entrance x 540 z -270 layer 0 camera keep facing 2

define Scene var[402]
actor 0 script 0:
    SetHiddenModel
    MusicLoad #56
    DisableTalk
    SetVarTrue Scene
    End

; The party: Elly alone, as the chair leaves it, in the hangar's own order of actors.
{PARTY}
""" + "".join(f"""; {name}.
actor {a} script 0:
    SetModel #{model}
    SetPosition #{x} #{z}
    SetFacingCode {facing}
    SetMessageFace #{face}
    End
actor {a} script 2:
    DisableControls
    FaceActor party0
    MessageAtActorPortrait self {idle} {face}
    WaitMessageClosed
    EnableControls
    End
""" for a, model, x, z, facing, name, face, idle in UNIT) + """
; Two of Shevat's own, at the gears.
actor 17 script 0:
    SetModel #1
    SetPosition #305 #600
    SetFacingCode 4
    End
actor 17 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Mechanic 0
    WaitMessageClosed
    EnableControls
    End
actor 18 script 0:
    SetModel #3
    SetPosition #380 #400
    SetFacingCode 4
    End
actor 18 script 2:
    DisableControls
    FaceActor party0
    MessageAtActor self Watchman 0
    WaitMessageClosed
    EnableControls
    End

; Before her unit: the farewell, the chair's scene, then the departure's page and Golgoda.
actor 19 script 0:
    SetHiddenModel
    SetPosition #600 #-270
    SetStateFlags 0 0x2000
    SetStateFlags 3 0x4
    SetCollisionSize 20 10 120 0
    SetCollisionFlags #1
    End
; Her arrival: the chair's page of the climb and the call, read beside her (a window closes at once when its speaker
; is off screen, so the page's actor stands where she comes in).
actor 20 script 0:
    SetHiddenModel
    DisableTalk
    SetPosition #-1031 #-268
    End
actor 20 script 1:
    DisablePlayer
    Wait #30
    SetWindowLayoutVar #0 #0 #0 #0 #1
    MessageCentered Ascend 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    SetVarFalse Scene
    EnablePlayer
    StopAndHalt
actor 19 script 3:
    If Scene == #0 else Begun
    SetVarTrue Scene
    DisablePlayer
    Wait #20
""" + "".join(f"    MessageAtActorPortrait {anchor} Line{n} {face}\n    WaitMessageClosed\n" for n, anchor, face in [
    (60, 'actor12', 65), (61, 'actor2', 1), (62, 'actor2', 1), (63, 'actor13', 69), (64, 'actor2', 1), (65, 'actor14', 67),
    (66, 'actor2', 1), (67, 'actor12', 65), (68, 'actor2', 1), (69, 'actor15', 68), (70, 'actor2', 1), (71, 'actor2', 1),
    (72, 'actor12', 65), (73, 'actor2', 1), (74, 'actor16', 66), (75, 'actor2', 1), (76, 'actor13', 69), (77, 'actor2', 1),
    (78, 'actor2', 1), (79, 'actor2', 1), (80, 'actor15', 68), (81, 'actor2', 1), (82, 'actor2', 1), (83, 'actor12', 65),
    (84, 'actor2', 1)]) + """    Wait #30
    SetWindowLayoutVar #0 #0 #0 #0 #1
    MessageCentered Depart 83
    WaitMessageClosed
    SetWindowLayoutVar #0 #0 #0 #0 #0
    ScreenFade #1 #0 #0 #0 #45
    Wait #45
    GearMode 1
    SetSlotInGear #0
    SetSlotInGear #1
    SetSlotInGear #2
    SetVar var[000] #290
    ChangeMap #619 #3
    StopAndHalt
Begun:
    End
"""
docs['golgoda-hangar.txt'] = finish(hangar.replace('{PARTY}', party), 21)

for name, text in docs.items():
    check_widths(name, text)
    open(OUT + name, 'w').write(text)
    print(name, len(text.splitlines()), 'lines')
