# This class manage the simulation
from grid import Grid 
from fish import Fish
class World:
    def __init__(self, grid: Grid) -> None:

        
        my_fish = Fish(12,12,1)
        my_fish.move(15,15)

        my_grid.affect_entity(1,12)
        my_grid.display()

my_grid = Grid(20)
w = World(my_grid)