from pyray import * #type:ignore
from typing import Any
import random

# laser's game of evolution
# designed and implemented by las-r

# HOW IT WORKS
# Cells can be either empty or living. If they're empty, then that's that. But,
# if they're living, then they have a species. There are 8 living species. The
# species are categorized into 3 groups: Swarms, Armors, and Reapers. Swarms
# are especially good at multiplying and spreading. However, they're kept in
# check by the Armors, which are good are fortifying, acting as a barrier to
# the Swarms' spread. Both Armors are kept in check by Reapers, which require
# sustenance. Reapers are predatory, they consume other cells to reproduce.
# Each cell has chance to mutate into a different species, up to 2 notches up
# or down. This chance is defined by the Radiation value. While there is a base
# value, this can be increased by the user. Also, the affects of Radiation
# increase as the density of cells increase, which drives evolution. You, as
# the user have been given the ability to blast the Dish with radiation. This
# leads to some interesting behaviors that I myself didn't intend to occur, yet
# they do. For example, Swarms are quite resistant to radiation, since they
# have a fairly low density. Also, it appears that among the armors, Yellow
# cells absolutely dominate. This, in retrospect, should've been expected as
# the rules favor origin over fortification, and Yellow borders the Swarms.
# Swarms appear to be fairly competitive, though. Red generally wins, as
# expected, but Orange definitely puts up a good fight. In the Reapers, White
# is the apex predator, which is expected as the armors are especially
# susceptible to it. Overall, making this game has been really interesting and
# a great learning process for emergent behaviors.

# settings
WIDTH, HEIGHT = 800, 800
TW, TH = 10, 10
GW, GH = WIDTH // TW, HEIGHT // TH
BASEMUTRATE = 0.005

# constants
COLORS = [
    BLACK,
    RED,     # Swarm
    ORANGE,  # Swarm
    YELLOW,  # Armor
    GREEN,   # Armor
    BLUE,    # Armor
    VIOLET,  # Reaper
    PINK,    # Reaper
    WHITE    # Reaper
]
DIRS = [
    Vector2(0, 1), Vector2(1, 1), Vector2(1, 0), Vector2(1, -1),
    Vector2(0, -1), Vector2(-1, -1), Vector2(-1, 0), Vector2(-1, 1),
]

# helper functions
def getneighbors(dish, x, y):
    colors = []
    for d in DIRS:
        c = dish[(y + int(d.y)) % GH][(x + int(d.x)) % GW]
        if c > 0:
            colors.append(c)
    return colors

# init
init_window(WIDTH, HEIGHT, "Game of Mutation")
set_target_fps(30)

# create the world
dish = [[0 for _ in range(GW)] for _ in range(GH)]
for _ in range(15):
    cx, cy = random.randint(10, GW-10), random.randint(10, GH-10)
    starting_species = random.randint(1, 4)
    for y in range(cy-5, cy+5):
        for x in range(cx-5, cx+5):
            if random.random() < 0.7:
                dish[y][x] = starting_species
t = 0

while not window_should_close():
    # input
    if is_key_pressed(KeyboardKey.KEY_R):
        dish = [[0 for _ in range(GW)] for _ in range(GH)]
        for _ in range(15):
            cx, cy = random.randint(10, GW-10), random.randint(10, GH-10)
            starting_species = random.randint(1, 4)
            for y in range(cy-5, cy+5):
                for x in range(cx-5, cx+5):
                    if random.random() < 0.7:
                        dish[y][x] = starting_species
        t = 0
    manualrad = is_key_down(KeyboardKey.KEY_SPACE)
    
    # drawing
    begin_drawing()
    clear_background(COLORS[0])
    for y, row in enumerate(dish):
        for x, tile in enumerate(row):
            if tile:
                draw_rectangle(x * TW, y * TH, TW, TH, COLORS[tile])
    draw_text(f"T: {t} | Hold SPACE for a radiation blast", 
              10, 10, 20, RAYWHITE)
    end_drawing()
    
    # set up calculation
    ndish = [[0 for _ in range(GW)] for _ in range(GH)]
    for y in range(GH):
        for x in range(GW):
            current = dish[y][x]
            ncols = getneighbors(dish, x, y)
            count = len(ncols)
            swarms = sum(1 for c in ncols if 1 <= c <= 2)
            armors = sum(1 for c in ncols if 3 <= c <= 5)
            reapers = sum(1 for c in ncols if 6 <= c <= 8)
            ncell = 0
            
            # living
            if current > 0:
                # swarms
                if current <= 2:
                    if 1 <= count <= 2 and reapers == 0:
                        ncell = current
                    elif reapers > 0: 
                        ncell = max(ncols)
                        
                # armors
                elif current <= 5:
                    if 2 <= count <= 6:
                        if reapers >= 2:
                            ncell = max(c for c in ncols if c >= 6)
                        else:
                            ncell = current
                            
                # reapers
                else:
                    if count >= 1 and (swarms > 0 or armors > 0):
                        ncell = current
                    else:
                        ncell = 0
            
            # birth
            else:
                if count == 2 and swarms >= 2:
                    ncell = random.choice([c for c in ncols if c <= 2])
                elif count == 3 and armors >= 2:
                    ncell = max(set(ncols), key=ncols.count)

            # radiation
            if ncell > 0:
                cellradrisk = BASEMUTRATE * (count + 1)
                if manualrad:
                    cellradrisk *= 10
                if random.random() < cellradrisk:
                    mutation = random.choice([-2, -1, 1, 2])
                    ncell = min(max(ncell + mutation, 1), 8)
            
            # set cell
            ndish[y][x] = ncell
            
    # update dish
    dish = ndish
    t += 1

# deinit
close_window()