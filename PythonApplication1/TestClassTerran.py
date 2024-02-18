import sc2
# from sc2 import run_game, maps, Race, Difficulty
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer, Human
import random

# Terran
import easy
from easy import MarineReaperBotEasy
import TerranMedium
from TerranMedium import TerranMediumAI
import CentipedeBot
from CentipedeBot import CentipedeBotAI
import CatipillarBot
from CatipillarBot import CatipillarAI
import MothBot
from MothBot import MothAI

# Zerg
# I'm too lazy to pull import these

# Protoss
# I'm too lazy to pull import these

"""Map Notes"""
# 1
# (4)Darkness Sanctuary LE
# Players: 4
# Main Ramps: NWDown, NEDown, SEDown, SWDown
# Symmetry: Rotational(90)
# Aesthetic: Dark
# Good map for testing ramps placements.
# Good map for testing how an AI responds to bad rally placements(REACTION TIME)
# Difficult map for rally placements
# Difficult map for scouting(4 players and walls are not good for reapers

# 2
# (2)Dreamcatcher LE
# Players: 2
# Main Ramps: NE, NE
# Symmetry: Mirror(Diagonal NE)
# Aesthetic: Green with lines. Shaped like a dreamcatcher
# Easy Map for conceptual Ramp placement because all main ramps face the same way
# Easy Map for rally placement because the first 32usual bases for expand_now function are on a trail to enemy base.

# 3
# Abyssal Reef LE
# Players: 2
# Main Ramps: SE, NW
# Symmetry: Rotational(180)
# Aesthetic: AMAZING UNDERWATER LAND!!!
# Easy Map for presentation not crashing or misdoing actions because the API makers test here for a few things
# Good map for testing scouting because experimentation shows that the AI is good at deflecting reapers on this map.

# 4
# (2) Acid Plant LE
# Players: 2
# Main Ramps: NE, SW
# Symmetry: Rotational(180)
# Aesthetic: Industrial Pollution Land
# Good map for testing uncommon two ramp positions.
# Difficult map for building placement because the bot has trouble finding landing spots for building and add on.

# 5
# (2)16-Bit LE
# Players: 2
# Main Ramps: NW, SE
# Symmetry: Rotational(180, Red Blue)
# Aesthetic: It's an retro computer-land world with a lot squares. One side is red and the other is blue.
# Good map for seeing how an AI handles a pocket base
# Good map for seeing how an AI handles 2 main base ramps(the correct one is cached in game data and easy to call api)
# Easy map for drop strats into natural
# Every Zerg commentator hates this map for Zerg players because of how easy it is for the pocket base to get harassed

# 6
# Fracture LE
# Players: 2
# Main Ramps: SE, NW
# Symmetry: Rotational(180)
# Aesthetic: It's frozen
# Good map for proxy strategies because of how the 2nd and 3rd expansion are located and their ramps.

# 7
# Frost LE
# Players: 4
# Main Ramps: SW, SE, NE, NW
# Symmetry: Mirror(X), Mirror(Y)
# Aesthetic: It has a lot of cold stuff. There is a mix of spooky elements but not enough to change the theme.
# Good map for testing building placement and landing locations to limited building space in 2nd expansion and weird elevation.
# Good map for testing ramp placement do to having all four ramp directions and weird elevation.
# Good map for testing pathing related functions such as rally and defend because of how weird the expansions are spaced and how weird the elevation is.
# Easy map for siege tanks and other AoE units because of narrow passages.
# Easy map for reaper focused play because of weird elevation.
# Bad map for having a normal game.

# 8
# Sequencer LE
# Players: 2
# Main Ramps: SW, NE
# Symmetry: Rotational(180)
# Aesthetic: It has a lot of space stuff and elevation changes look like a pattern
# Good map for testing how a bot handles destructible rock walls.
# Good map for testing how a bot handles changes in elevation.
# Easy map for Reapers because almost every wall is 1 elevation jump.

# 9
# (2)Red Shift LE
# Players: 2
# Main Ramps: NE(LSW), SE(LNW)
# Symmetry: Mirror(Y)
# Aesthetic: It's red
# Good map for testing fail safes because my normal building placements fail here.
# Good map for testing weird game and obscure strategies.
# Bad map for pretty much everything

# 10
# Neon Violet Square LE
# Players: 2
# Main Ramps: SW, NE
# Symmetry: Rotational(180)
# Aesthetic: Pretty colors and glowy technology
# Good map for testing how AI handles filter tiles that let the small units in.
# Easy map for defensive playstyle because it has two easy to defend expansions.
# Hard map for placing buildings as terran because the main has small amounts of width.

"""TEST SCRIPT BELOW"""
enemy = ""
enemynumber = random.randint(1, 4)
if enemynumber == 1:
    enemy = Race.Random
elif enemynumber == 2:
    enemy = Race.Terran
elif enemynumber == 3:
    enemy = Race.Zerg
elif enemynumber == 4:
    enemy = Race.Protoss
#mapnumber = random.randint(1, 10)
mapname = ""
"""if mapnumber == 1:
    mapname = "(4)Darkness Sanctuary LE"
elif mapnumber == 2:
    mapname = "(2)Dreamcatcher LE"
elif mapnumber == 3:
    mapname = "Abyssal Reef LE"
elif mapnumber == 4:
    mapname = "(2)Acid Plant LE"
elif mapnumber == 5:
    mapname = "(2)16-Bit LE"
elif mapnumber == 6:
    mapname = "Fracture LE"
elif mapnumber == 7:
    mapname = "Frost LE"
elif mapnumber == 8:
    mapname = "Sequencer LE"
elif mapnumber == 9:
    mapname = "(2)Red Shift LE"
elif mapnumber == 10:
    mapname = "Neon Violet Square LE"""
# mapname = "" # override for testing specific problem
mapname = "Equilibrium512AIE"

print("Battling:")
print(enemy)
print("Map:")
print(mapname)
print("-------")
# note: There is known bug in the python sc2 where hard -> harder and harder -> very hard

"""
run_game(maps.get(mapname), [
    Bot(Race.Terran, MothAI()),
    Computer(enemy, Difficulty.VeryHard)
], realtime=False)
"""
"""
print("ignoring rng for player race")
run_game(maps.get(mapname), [
    Human(Race.Terran),
    Bot(Race.Terran, MothAI())
], realtime=True)
"""
"""run_game(maps.get(mapname), [
    Bot(Race.Terran, MothAI()),
    Computer(Race.Random, Difficulty.Hard)
], realtime=False)"""
run_game(maps.get(mapname), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=False)
#Test cases used
"""
# Test case used for picking a randomized race(Terran, Zerg, Protoss, Random)
# Possible Matchups are 1/4 Terran, 1/4 Zerg, 1/4 Protoss, 1/12 RandomTerran, 1/12 Random Zerg, 1/12 Random Protoss
enemy = ""
enemynumber = random.randint(1, 4)
if enemynumber == 1:
    enemy = Race.Random
elif enemynumber == 2:
    enemy = Race.Terran
elif enemynumber == 3:
    enemy = Race.Zerg
elif enemynumber == 4:
    enemy = Race.Protoss
mapnumber = random.randint(1, 5)
mapname = ""
if mapnumber == 1:
    mapname = "(4)Darkness Sanctuary LE"
elif mapnumber == 2:
    mapname = "(2)Dreamcatcher LE"
elif mapnumber == 3:
    mapname = "Abyssal Reef LE"
elif mapnumber == 4:
    mapname = "(2)Acid Plant LE"
elif mapnumber == 5:
    mapname = "(2)16-Bit LE"
print("Battling:")
print(enemy)
print("Map:")
print(mapname)
run_game(maps.get(mapname), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(enemy, Difficulty.Harder)
], realtime=False)

# Test case used for best of 3 and 5 for Terran vs. Random
run_game(maps.get(mapname), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Random, Difficulty.Harder)
], realtime=False) 

# Test case used for best of 3 and 5 for Terran vs. Terran
run_game(maps.get(mapname), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Terran, Difficulty.Harder)
], realtime=False)

# Test case used for best of 3 and 5 for Terran vs. Zerg
run_game(maps.get(mapname), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Zerg, Difficulty.Harder)
], realtime=False)

# Test case used for best of 3 and 5 for Terran vs. Protoss
run_game(maps.get(mapname), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Protoss, Difficulty.Harder)
], realtime=False)
"""
# example games
"""
run_game(maps.get("(2) Acid Plant LE"), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Random, Difficulty.Hard)
], realtime=True)

run_game(maps.get("(4)Darkness Sanctuary LE"), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Random, Difficulty.Hard)
], realtime=True)

run_game(maps.get("(2)16-Bit LE"), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Random, Difficulty.Hard)
], realtime=True)

run_game(maps.get("(2)Dreamcatcher LE"), [
    Bot(Race.Terran, CatipillarAI()),
    Computer(Race.Random, Difficulty.Hard)
], realtime=False)
"""