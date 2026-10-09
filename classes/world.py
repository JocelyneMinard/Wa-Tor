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

        my_grid.display()


    @property
    def all_entities(self):
        self.all_entities_dict = {}
        for fid, fobj in self.fish_dict.items():
            self.all_entities_dict[("fish", fid)] = fobj
        for sid, sobj in self.shark_dict.items():
            self.all_entities_dict[("shark", sid)] = sobj
        return self.all_entities_dict

    # mouvement fish and shark
    def move_entities(self):
        for entity_id, entity_obj in self.all_entities.items():
            x = entity_obj.get_x()
            y = entity_obj.get_y()
            type = entity_obj.get_type()
            new_coord = my_grid.move(x, y)
            entity_obj.x = new_coord[0]
            entity_obj.y = new_coord[1]
            my_grid.affect_entity(new_coord[0],new_coord[1], type)
           
        
        my_grid.display()

my_grid = Grid(10)
w = World(my_grid, 10)


for i in range(5):
    print(f"--- Tour {i+1} ---")
    w.move_entities()
    print(" ")