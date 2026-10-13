# This class manages the simulation

from classes.fish import Fish
from classes.shark import Shark
import random

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 20
        self.population_init_shark = 2
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
        # fix list of dict shark
        for entity_id in list(self.shark_dict.keys()):
            if entity_id in self.shark_dict:
                self.move(self.shark_dict[entity_id])
                
        # fix list of dict fish
        for entity_id in list(self.fish_dict.keys()):
             if entity_id in self.fish_dict:
                self.move(self.fish_dict[entity_id])
        self.my_grid.display()

    def move(self, entity):
        x = entity.get_x()
        y = entity.get_y()
        type = entity.get_type()
        empty_cells, fish_cells  = self.my_grid.check_possible_moves(x, y)
        moved = False
        dx = 0
        dy = 0

        match type:
            case "fish":
                if(empty_cells):
                    dx, dy = random.choice(empty_cells)
                    can_reproduce_fish = Fish.reproduce(entity, self.turn) 
                    if can_reproduce_fish :  
                        new_id = max(self.fish_dict.keys(), default=-1) + 1
                        self.fish_dict[new_id] = Fish(x, y)
                    else:
                        self.my_grid.affect_entity(x, y, "empty")
                    moved = True
            case "shark":
                if (Shark.get_stamina(entity) > 0):
                    if fish_cells:                    
                        dx, dy = random.choice(fish_cells)
                        # Calcul de la position du poisson à manger (avec wrapping)
                        target_x = (x + dx) % self.grid_size
                        target_y = (y + dy) % self.grid_size
                        # Trouver et supprimer le poisson du dictionnaire
                        Shark.eat_fish(entity, target_x, target_y, self.fish_dict.items(),  self.fish_dict)
                        moved = True
                        self.my_grid.affect_entity(x, y, "empty")
                    elif(empty_cells):
                        dx, dy = random.choice(empty_cells)
                        shark_can_reproduce = Shark.reproduce(entity, self.turn)
                        if shark_can_reproduce :
                            new_id = max(self.shark_dict.keys(), default=-1) + 1
                            self.shark_dict[new_id] = Shark(x, y) 
                        else:
                            self.my_grid.affect_entity(x, y, "empty")
                        Shark.decrease_stamina(entity)
                        moved = True
                else:
                    for shark_id, shark_obj in list(self.shark_dict.items()):
                        if shark_obj == entity:  # Plus simple et plus sûr que de comparer x et y
                            Shark.remove_shark(entity, self.shark_dict, shark_id)
                            self.my_grid.affect_entity(x, y, "empty")
                            break 
                
        if (moved == True ):
            # Updating positions with wrapping
            x = (x + dx) % self.grid_size
            y = (y + dy) % self.grid_size
            entity.x = x    #update  in dictonary the entity position
            entity.y = y
            self.my_grid.affect_entity(x, y, type)
            return(x, y)
        
