import pygame as pg
from random import randint

# Display window size
WIDTH = 1900
HEIGHT = 1000

COLOR = [(0, 0, 0), (255, 255, 255)]

# "Adjustable" constants (during runtime using keys)
CELL_SIZE = 7
FPS = 1000.0

# Rules
BIRTH_LIST = [3]
SURVIVE_LIST = [2, 3]

# Initial display range
num_rows = HEIGHT // (CELL_SIZE + 1)
num_cols = WIDTH // (CELL_SIZE + 1)
top_left = (-(num_cols // 2), -(num_rows // 2))
center = (0, 0)

# cells value list element indexes
CURR_STATE = 0
NEXT_STATE = 1
NUM_NEIGHBORS = 2


def create_random():
    # Create random cells
    for i in range(30000):
        # grid_x, grid_y = randint(-num_cols // 2, num_cols // 2), randint(-num_rows // 2, num_rows // 2)
        grid_x, grid_y = randint(top_left[0], top_left[0] + num_cols), randint(top_left[1], top_left[1] + num_rows)
        if (grid_x, grid_y) not in cells:
            cells[(grid_x, grid_y)] = [1, 1, 0]
        else:
            cells[(grid_x, grid_y)][NEXT_STATE] = 1 - cells[(grid_x, grid_y)][CURR_STATE]
        update_cell((grid_x, grid_y))
    pg.display.flip()


def draw_cell(x, y, state):
    # No need to draw if cell does not appear in the window
    if top_left[0] <= x < (top_left[0] + num_cols) and top_left[1] <= y < (top_left[1] + num_rows):
        # Calculate screen offsets
        screen_x = (x - top_left[0]) * (CELL_SIZE + 1)
        screen_y = (y - top_left[1]) * (CELL_SIZE + 1)
        pg.draw.rect(screen, COLOR[state], (screen_x, screen_y, CELL_SIZE, CELL_SIZE))


def move_screen(center_point: tuple):
    global top_left, num_cols, num_rows
    num_rows = HEIGHT // (CELL_SIZE + 1)
    num_cols = WIDTH // (CELL_SIZE + 1)
    top_left = (-(num_cols // 2) + center_point[0], -(num_rows // 2) + center_point[1])
    screen.fill((0, 0, 0))
    for curr_cell in cells:
        draw_cell(curr_cell[0], curr_cell[1], cells[curr_cell][CURR_STATE])
    pg.display.flip()


def remove_cells():
    global cells_to_remove
    # Remove inactive cells with no neighbors
    for curr_cell in cells_to_remove:
        if curr_cell in cells:
            if cells[curr_cell][CURR_STATE] == 0 and cells[curr_cell][NUM_NEIGHBORS] == 0:
                cells.pop(curr_cell)


def set_next_state(cell_parm: tuple):
    curr_cell = cells[cell_parm]
    if curr_cell[CURR_STATE] == 1:
        if curr_cell[NUM_NEIGHBORS] not in SURVIVE_LIST:
            curr_cell[NEXT_STATE] = 0
            cells_to_update.append(cell_parm)
    elif curr_cell[NUM_NEIGHBORS] in BIRTH_LIST:
        curr_cell[NEXT_STATE] = 1
        cells_to_update.append(cell_parm)


def toggle_cell(mouse_pos: tuple):
    x = mouse_pos[0] // (CELL_SIZE + 1) + top_left[0]
    y = mouse_pos[1] // (CELL_SIZE + 1) + top_left[1]
    if (x, y) not in cells:
        cells[(x, y)] = [1, 1, 0]
    else:
        cells[(x, y)][NEXT_STATE] = 1 - cells[(x, y)][CURR_STATE]
    update_cell((x, y))
    remove_cells()
    pg.display.flip()


def update_cell(cell_parm: tuple):
    global live_cells
    x0, y0 = cell_parm[0], cell_parm[1]
    curr_cell = cells[cell_parm]
    curr_cell[CURR_STATE] = curr_cell[NEXT_STATE]
    # Update each of current cell's neighbors' num_neighbors based on current cell's state
    for y in range(y0 - 1, y0 + 2):
        for x in range(x0 - 1, x0 + 2):
            if curr_cell[CURR_STATE] == 1:
                if (x, y) not in cells:
                    # Create cell for neighbor
                    cells[(x, y)] = [0, 0, 1]
                else:
                    cells[(x, y)][NUM_NEIGHBORS] += 1
            else:
                if not (x == x0 and y == y0):
                    # if (x, y) in cells:
                    cells[(x, y)][NUM_NEIGHBORS] -= 1
                if cells[(x, y)][CURR_STATE] == 0 and cells[(x, y)][NUM_NEIGHBORS] == 0:
                    # Neighbor is inactive and has no active neighbors, so remove
                    cells_to_remove.append((x, y))
    if curr_cell[CURR_STATE] == 1:
        curr_cell[NUM_NEIGHBORS] -= 1  # Don't count itself
        live_cells += 1
    else:
        live_cells -= 1
    draw_cell(x0, y0, curr_cell[CURR_STATE])


# MAIN PROGRAM
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
frame = 0

# Dictionary formatted as {(x, y): [curr_state, next_state, num_neighbors]}
cells = {}
cells_to_update = []
cells_to_remove = []
live_cells = 0

pg.display.flip()
running = True
paused = True
single_frame = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE:
                paused = not paused
            # Arrow keys move display 10% over
            elif event.key == pg.K_LEFT:
                center = (center[0] - (num_cols // 10), center[1])
                move_screen(center)
            elif event.key == pg.K_RIGHT:
                center = (center[0] + (num_cols // 10), center[1])
                move_screen(center)
            elif event.key == pg.K_UP:
                center = (center[0], center[1] - (num_rows // 10))
                move_screen(center)
            elif event.key == pg.K_DOWN:
                center = (center[0], center[1] + (num_rows // 10))
                move_screen(center)
            # PgUp/PgDn change block size
            elif event.key == pg.K_PAGEUP:
                CELL_SIZE += 1
                move_screen(center)
            elif event.key == pg.K_PAGEDOWN:
                if CELL_SIZE > 1:
                    CELL_SIZE -= 1
                    move_screen(center)
            # +/- change frame rate
            elif event.key == pg.K_KP_PLUS:
                FPS *= 1.2
            elif event.key == pg.K_KP_MINUS:
                FPS /= 1.2
            elif event.key == pg.K_r:
                create_random()
            # Advance a single frame
            elif event.key == pg.K_s:
                paused = False
                single_frame = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            toggle_cell(event.pos)

    if not paused:
        frame += 1

        cells_to_update.clear()     # Clear list prior to each generation
        cells_to_remove.clear()

        # Evaluate all cells for next state
        for cell in cells:
            set_next_state(cell)

        # Update cells
        if len(cells_to_update) == 0:  # Nothing changed--stable state
            paused = True
        else:
            for cell in cells_to_update:
                if cell in cells:  # Needs to be checked because the cell may have been removed by a previous update
                    update_cell(cell)

        # Remove inactive cells with no neighbors
        remove_cells()

        if live_cells == 0:
            paused = True

        if single_frame:
            paused = True
            single_frame = False

        pg.display.flip()
        clock.tick(int(FPS))

        pg.display.set_caption(f"Current Frame: {frame:6d}     FPS: {clock.get_fps():3.2f}     " +
                               f"Live Cells: {live_cells:6d}     Eval List: {len(cells):6d}     Center: {center}     ")
