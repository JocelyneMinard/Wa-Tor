# This class manages the simulation
from grid import Grid 
from fish import Fish
from shark import Shark
import random
import os, time

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 30
        self.population_init_shark = 1
        self.my_grid = my_grid  
        self.grid_size = grid_size
        self.fish_dict = {}
        self.shark_dict = {}
        self.turn = 0
        my_grid_empty_cells = my_grid.check_grid()

        if int(self.population_init_fish * 0.6) >= self.grid_size:
            self.population_init_fish = int(self.population_init_fish * 0.6)
        for i in range(self.population_init_fish):
            if my_grid_empty_cells:
                x, y = random.choice(my_grid_empty_cells)
                my_grid_empty_cells.remove((x, y))  # CORRECTION: On enlève la case pour éviter les doublons
                self.my_grid.affect_entity(x, y, "fish")
                self.fish_dict[i] = Fish(x, y)

        # Remplissage des Requins
        if int(self.population_init_shark * 0.3) >= self.grid_size:
            self.population_init_shark = int(self.population_init_shark * 0.3)
        for i in range(self.population_init_shark):
            if my_grid_empty_cells:
                x, y = random.choice(my_grid_empty_cells)
                my_grid_empty_cells.remove((x, y))  # CORRECTION: On enlève la case
                self.my_grid.affect_entity(x, y, "shark")
                self.shark_dict[i] = Shark(x, y)
        my_grid.display()


    # mouvement fish and shark
    def move_entities(self):
        for entity_id, entity_obj in self.shark_dict.items():
            self.move(entity_obj)
        for entity_id, entity_obj in self.fish_dict.items():
            if entity_id in self.fish_dict:
                # check if fish exist , he cqn be eat by shark before
                self.move(entity_obj)
        my_grid.display()

    def move(self, entity):
        x = entity.get_x()
        y = entity.get_y()
        type = entity.get_type()
        empty_cells, fish_cells  = my_grid.check_possible_moves(x, y)
        moved = False
        dx = 0
        dy = 0

        match type:
            case "fish":
                if(empty_cells):
                    dx, dy = random.choice(empty_cells)
                    my_grid.affect_entity(x, y, "empty")
                    moved = True
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
                        moved = True
                elif(empty_cells):
                    dx, dy = random.choice(empty_cells)
                    moved = True
                
        if (moved == True ):     
            my_grid.affect_entity(x, y, "empty")
            # Updating positions with wrapping
            x = (x + dx) % self.grid_size
            y = (y + dy) % self.grid_size
            entity.x = x    #update  in dictonary the entity position
            entity.y = y
            my_grid.affect_entity(x, y, type)
            return(x, y)
        

grid_size = 5
my_grid = Grid(grid_size)
w = World(my_grid, grid_size)



while w.turn < 10:
    #os.system('clear') 
    w.turn += 1
    print(f"--- Tour {w.turn} ---")
    w.move_entities()
    time.sleep(1)