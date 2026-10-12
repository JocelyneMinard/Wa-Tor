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
        self.my_grid = my_grid  # Stockage de la grille dans l'instance
        self.grid_size = grid_size
        self.fish_dict = {}
        self.shark_dict = {}
        my_grid_empty_cells = my_grid.check_grid()

        if self.population_init_fish >= self.grid_size:
            self.population_init_fish = int(self.population_init_fish * 0.7)
            print(self.population_init_fish)
        for i in range(self.population_init_fish):
            if my_grid_empty_cells:
                x, y = random.choice(my_grid_empty_cells)
                my_grid_empty_cells.remove((x, y))  # CORRECTION: On enlève la case pour éviter les doublons
                self.my_grid.affect_entity(x, y, "fish")
                self.fish_dict[i] = Fish(x, y)

        # Remplissage des Requins
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
            self.move(entity_obj)
        my_grid.display()

    def move(self, entity):
        x = entity.get_x()
        y = entity.get_y()
        type = entity.get_type()
        empty_cells, fish_cells  = my_grid.check_possible_moves(x, y)

        match type:
            case "fish":
                if(empty_cells):
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
                elif(empty_cells):
                    dx, dy = random.choice(empty_cells)
                else:
                    dy = 0
                    dx = 0
                my_grid.affect_entity(x, y, "empty")

        # Updating positions with wrapping
        x = (x + dx) % self.grid_size
        y = (y + dy) % self.grid_size
        entity.x = x
        entity.y = y
        my_grid.affect_entity(x, y, type)
        return(x, y)
        

grid_size = 5
my_grid = Grid(grid_size)
w = World(my_grid, grid_size)


turn = 0
while turn < 10:
    #os.system('clear') 
    turn += 1
    print(f"--- Tour {turn} ---")
    w.move_entities()
    time.sleep(1)