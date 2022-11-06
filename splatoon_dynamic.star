
load("render.star", "render")
load("encoding/base64.star", "base64")

def main():
    return render.Root(
        max_age=60,
        delay=125,
        child=render.Marquee(
            height=32,
            offset_start = 32,
            offset_end = 32,
            scroll_direction="vertical",
            child=render.WrappedText("""Nov 5, 2022, 11:00 AM - Nov 7, 2022, 2:00 AM

STAGE:
Spawning Grounds

LOADOUT:
Sploosh-o-matic, Luna Blaster, Undercover Brella, Splat Charger

REWARD(S):
Brain Strainer
-------

Nov 7, 2022, 2:00 AM - Nov 8, 2022, 6:00 PM

STAGE:
Sockeye Station

LOADOUT:
Splat Roller, Dualie Squelchers, Nautilus 47, Heavy Splatling

REWARD(S):
Brain Strainer
-------

Nov 8, 2022, 6:00 PM - Nov 10, 2022, 10:00 AM

STAGE:
Gone Fission Hydroplant

LOADOUT:
Tri-Slosher, L-3 Nozzlenose, Splat Brella, .96 Gal

REWARD(S):
Brain Strainer
-------

Nov 10, 2022, 10:00 AM - Nov 12, 2022, 2:00 AM

STAGE:
Spawning Grounds

LOADOUT:
Splattershot Jr., Sloshing Machine, Range Blaster, Goo Tuber

REWARD(S):
Brain Strainer
-------

Nov 12, 2022, 2:00 AM - Nov 13, 2022, 6:00 PM

STAGE:
Sockeye Station

LOADOUT:
Splat Dualies, Carbon Roller, Splattershot Pro, Splat Charger

REWARD(S):
Brain Strainer""", width=60)
        )
    )
