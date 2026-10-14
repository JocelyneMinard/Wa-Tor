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
    print(f"--------------Turn : {w.turn}--------------")
    print(f"Fish number : {len(w.fish_dict)}")
    print(f"Shark number : {len(w.shark_dict)}")
    time.sleep(0.7)
