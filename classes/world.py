# This class manage the simulation
from grid import Grid 
from fish import Fish
from shark import Shark
import random

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 5
        self.population_init_shark = 1
        self.grid_size = grid_size
        self.fish_dict = {}
        self.shark_dict = {}

        for i in range(self.population_init_fish) :
            x = random.randint(0, self.grid_size -1)
            y = random.randint(0, self.grid_size -1)
            my_grid.affect_entity(x,y, "fish")
            self.fish_dict[i] = Fish(x,y)

        for i in range(self.population_init_shark) :
            x = random.randint(0, self.grid_size -1)
            y = random.randint(0, self.grid_size -1)
            my_grid.affect_entity(x,y, "shark")
            self.shark_dict[i] = Shark(x,y)

        @property
        def fish_dict(self):
            return self.fish_dict

        @property
        def shark_dict(self):
            return self.shark_dict

        my_grid.display()
        
    # mouvement fish and shark
    def move_entities(self, entity):
        for entity_id, entity_obj in entity.items():
            x = entity_obj.get_x()
            y = entity_obj.get_y()
            type = entity_obj.get_type()
            new_coord = my_grid.move(x, y)
            my_grid.affect_entity(new_coord[0],new_coord[1], type)
           
        
        my_grid.display()

my_grid = Grid(10)
w = World(my_grid, 10)

entities = w.fish_dict | w.shark_dict

for i in range(5):
    w.move_entities(entities)
    print(" ")