# GameOfLife
Conway's Game of Life in Python (Unlimited Size) with PyGame

This is an unbounded implementation of GOL in Python. By "unbounded," I mean that it is not limited to the size of the screen. Cells can can move in any direction indefinitely and the number of cells is limited only by the amount of avaialable memory.

The only dependency is PyGame, which needs to be installed if you do not already have it (you should, it's awesome!).

I am not using a fixed-sized list for the cell data. This would not be practical to allow for the cells to grow and move indefinitely in any direction. The data structure I chose to hold the cells of interest is a Python dictionary. The key for each entry is a tuple of the (X, Y) grid position of the cell. The value is a list containing three elements: the cell's current state; its next state; and a running count of the number of live neighboring cells.

When you run the program, it starts off with an empty screen and the simulator paused. You can use the mouse to click on the screen and toggle the state of the cell at that position. Initially, the cell size is 1, which is not very convenient for trying to create a specific pattern. There are keys to change the displayed cell size (see below). There are constants defined at the beginning of the program where you can set the initial values for things, including the display size in pixels.

What I determined when thinking about which cells need to be considered for each generation and which don't is that the only cells you care about are active cells, or inactive cells with at least one live neighbor. The rest of the cells in the "universe" are inactive and cannot become active in the next generation.

Once you have a bunch of cells activated, you can unpause the simulation. For each generation, the cells are first evaluated to determine their next state. Once all the cells are evaluated, they are updated, having their current state set to the next state which was determined in the evaluation step. The display is also updated according to the new state.

For each cell in the dictionary, the rules are applied (a live cell survived if it has 2 or 3 neighbors but dies otherwise; a dead cell becomes alive if it has exactly 3 neighbors) by the "set_next_state" function. These rules are defined as constant lists at the top of the program. You can change them to see how it affects things. If the state of a cell has changed, it is added to a list called "cells_to_update". This allow for a nice performance improvement since typically, a fair percentage of cells of interest will not change.

After all the cells in the dictionary have been evaluated, the list of cells to be updated is used to call "update_cell". This function will set the cell's current state to the next state. It then updates the count of live neighbors of each of that cell's neighboring cells. If the cell has been activated, and if the dictionary does not currently contain an entry for a neighbor, the neighbor will be added to dictionary. If the cell has been deactivated, the neighbor count for each of the neighboring cells is decremented. If it becomes 0 (meaning no more live neighbors), the neighboring cell will be added to a list of "cells_to_remove)". Keeping a running count of each cell's active neighbors is another imnprovment over figuring out the count for each cell in each generation.

Following the update step, any cells in the cells_to_remove list will be removed from the cells dictionary, since they are no longer of interest (they are inactive and have no active neighbors).

After all the cell data has been updated, the display is updated with a call to PyGame's display.flip method. The clock.tick method is also called so that the maximum frame rate can be controlled and the actual frame rate displayed in the caption bar of the window.

There are a number of keys which can be used to control the running of the simlation. They are:
* ESCAPE -- Quit the program
* SPACE -- Pause/unpause the simulation
* Arrow Keys -- Pan the display in the appropriate direction
* PgUp/PgDn -- Increase/decrease the cell size
* Keypad +/- -- Increase/decrease the frame rate
* r -- Creates a set of random cells within the current display area. Most cells will die immediately. You can play around with the number of cells which get created (currently hardcoded as 30000). I should probably change it to be a percentage of the number of cells on the screen based on the current cell size. Maybe later.  :-)
* s -- Advance a single frame

Note the initial cell size and frame rate are specified at the top of the program.

The window caption displays some interesting information so you can see how the sim is progressing. On my computer, which is fairly new (Intel i7-11700K, 32GB RAM), with about 7000 live cells and a dictionary containing over 50000 cells of interest, I am getting better than 40 frames per second. Your mileage may vary.

As a final note, I am relatively new to Python, certainly not an expert. I am well aware that I did not set up a main() function and use the "IF __main__ == 'main'" construct, and that I used a numnber of global variables which is less than desirable. This was meant as a stand-alone program and I was trying to keep things as simple as possible. I am sure there are more "Pythonic" ways of doing things here. I would love any feedback as to how to improve this code. Hopefully, it's not total trash.
