# This class manage the simulation
from grid import Grid 
from fish import Fish
import random

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 5
        self.population_init_shark = 1
        self.grid_size = grid_size

        for i in range(self.population_init_fish) :
            x = random.randint(0, self.grid_size)
            y = random.randint(0, self.grid_size)
            my_grid.affect_entity(x,y, "fish")

        for i in range(self.population_init_shark) :
            x = random.randint(0, self.grid_size)
            y = random.randint(0, self.grid_size)
            my_grid.affect_entity(x,y, "shark")
        
        my_grid.display()

my_grid = Grid(20)
w = World(my_grid, 20)