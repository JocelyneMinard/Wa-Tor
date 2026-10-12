# This class manages the simulation
from grid import Grid 
from fish import Fish
from shark import Shark
import random
import os, time
import pprint

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 30
        self.population_init_shark = 1
        self.grid_size = grid_size
        self.fish_dict = {}
        self.shark_dict = {}
        my_grid_empty_cells = my_grid.check_grid()

        for i in range(self.population_init_fish) :
            if(my_grid_empty_cells):
                x, y = random.choice(my_grid_empty_cells)
                my_grid.affect_entity(x, y, "fish")
                self.fish_dict[i] = Fish(x,y)

        for i in range(self.population_init_shark) :
            if(my_grid_empty_cells):
                x, y = random.choice(my_grid_empty_cells)
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
        for entity_id, entity_obj in self.shark_dict.items():
            self.move(entity_obj)
        for entity_id, entity_obj in self.fish_dict.items():
            self.move(entity_obj)
        my_grid.display()

    def move(self, entity):
        x = entity.get_x()
        y = entity.get_y()
        type = entity.get_type()
        empty_cells, fish_cells  = my_grid.check_possible_moves(x, y)

        match type:
            case "fish":
                print(empty_cells)
                if(empty_cells):
                    print("pass not empty")
                    dx, dy = random.choice(empty_cells)
                    my_grid.affect_entity(x, y, "empty")
                else: 
                    #fish without empty cells around
                    dx = 0
                    dy = 0
            case "shark":
                if fish_cells:
                    dx, dy = random.choice(fish_cells)
                    # Calcul de la position du poisson à manger (avec wrapping)
                    target_x = (x + dx) % self.grid_size
                    target_y = (y + dy) % self.grid_size
                     # Trouver et supprimer le poisson du dictionnaire
                    for fid, fobj in list(self.fish_dict.items()):
                        if fobj.get_x() == target_x and fobj.get_y() == target_y:
                            Fish.remove_fish(self, self.fish_dict, fid)
                            break
                elif(empty_cells != ""):
                    dx, dy = random.choice(empty_cells)
                my_grid.affect_entity(x, y, "empty")

        # Updating positions with wrapping
        x = (x + dx) % self.grid_size
        y = (y + dy) % self.grid_size
        entity.x = x
        entity.y = y
        my_grid.affect_entity(x, y, type)
        return(x, y)
        

my_grid = Grid(5)
w = World(my_grid, 5)


turn = 0
while turn < 30:
    #os.system('clear') 
    turn += 1
    print(f"--- Tour {turn} ---")
    w.move_entities()
    time.sleep(1)