from classes.grid import Grid 
from classes.world import World 
import os, time

grid_size = 20
my_grid = Grid(grid_size)
w = World(my_grid, grid_size)


while True:
    os.system('clear') 
    w.turn += 1
    w.move_entities()
    time.sleep(0.7)
