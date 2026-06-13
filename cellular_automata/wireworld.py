from pyray import * #type:ignore

# wireworld
# designed by brian silverman
# implemented by las-r

# settings
WIDTH, HEIGHT = 800, 800
TW, TH = 20, 20
GW, GH = WIDTH // TW, HEIGHT // TH
SIMDELAY = 0.25

# constants
COLORS = [
    BLACK,
    BLUE,
    RED,
    YELLOW
]
DIRS = [
    Vector2(0, 1), Vector2(1, 1), Vector2(1, 0), Vector2(1, -1),
    Vector2(0, -1), Vector2(-1, -1), Vector2(-1, 0), Vector2(-1, 1),
]

# helper functions
def neighborheads(cells, x, y):
    heads = 0
    for d in DIRS:
        nx, ny = int(x + d.x), int(y + d.y)
        if 0 <= nx < GW and 0 <= ny < GH:
            if cells[ny][nx] == 1:
                heads += 1
    return heads

# init
init_window(WIDTH, HEIGHT, "Wireworld")
set_target_fps(60) # Keep this at 60 for beautiful, fluid responsive input

# variables
cells = [[0 for _ in range(GW)] for _ in range(GH)]
start = [[0 for x in range(GW)] for y in range(GH)]
paused = True

# main loop
simtimer = 0.0
lefttarget = 1
righttarget = 3
while not window_should_close():
    # input
    m = get_mouse_position()
    if paused:
        if 0 <= m.x < WIDTH and 0 <= m.y < HEIGHT:
            gx = int(m.x / TW)
            gy = int(m.y / TH)
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                lefttarget = (cells[gy][gx] + 1) % 4
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                cells[gy][gx] = lefttarget
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT):
                righttarget = (cells[gy][gx] - 1) % 4
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_RIGHT):
                cells[gy][gx] = righttarget
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_MIDDLE):
                cells[gy][gx] = 0
        if is_key_pressed(KeyboardKey.KEY_R):
            cells = [[start[y][x] for x in range(GW)] for y in range(GH)]
            paused = True
            simtimer = 0.0
        if is_key_pressed(KeyboardKey.KEY_C):
            cells = [[0 for _ in range(GW)] for _ in range(GH)]
            start = [[0 for _ in range(GW)] for _ in range(GH)]
            paused = True
            simtimer = 0.0
    if is_key_pressed(KeyboardKey.KEY_SPACE):
        if paused:
            start = [[cells[y][x] for x in range(GW)] for y in range(GH)]
            paused = False
        else:
            paused = True
            
    # calculation
    if not paused:
        simtimer += get_frame_time()
        if simtimer >= SIMDELAY:
            simtimer = 0.0
            ncells = [[0 for _ in range(GW)] for _ in range(GH)]
            for y, row in enumerate(cells):
                for x, cell in enumerate(row):
                    if cell == 1:
                        ncells[y][x] = 2
                    elif cell == 2:
                        ncells[y][x] = 3
                    elif cell == 3:
                        nh = neighborheads(cells, x, y)
                        if 1 <= nh <= 2:
                            ncells[y][x] = 1
                        else:
                            ncells[y][x] = 3
            cells = ncells
            
    # draw
    begin_drawing()
    clear_background(COLORS[0])
    for y, row in enumerate(cells):
        for x, cell in enumerate(row):
            if cell:
                draw_rectangle(x * TW, y * TH, TW, TH, COLORS[cell])
    draw_text(f"Paused: {paused}", 10, 10, 20, WHITE)
    end_drawing()

# deinit
close_window()