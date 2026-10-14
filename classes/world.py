# This class manages the simulation

from classes.fish import Fish
from classes.shark import Shark
import random

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 25
        self.population_init_shark = 5
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
                my_grid_empty_cells.remove((x, y))  # On enlève la case pour éviter les doublons
                self.my_grid.affect_entity(x, y, "fish")
                self.fish_dict[i] = Fish(x, y)

        # Remplissage des Requins
        if int(self.population_init_shark * 0.3) >= self.grid_size:
            self.population_init_shark = int(self.population_init_shark * 0.3)
        for i in range(self.population_init_shark):
            if my_grid_empty_cells:
                x, y = random.choice(my_grid_empty_cells)
                my_grid_empty_cells.remove((x, y))  # On enlève la case de la liste 
                self.my_grid.affect_entity(x, y, "shark")
                self.shark_dict[i] = Shark(x, y)
        my_grid.display()


    # mouvement fish and shark
    def move_entities(self):
        # fix list of dict shark
        for entity_id in list(self.shark_dict.keys()):
            if entity_id in self.shark_dict:
                self.move(self.shark_dict[entity_id], entity_id)
                
        # fix list of dict fish
        for entity_id in list(self.fish_dict.keys()):
             if entity_id in self.fish_dict:
                self.move(self.fish_dict[entity_id], entity_id)
        self.my_grid.display()

    def move(self, entity, entity_id):
        x = entity.get_x()
        y = entity.get_y()
        entity_type = entity.get_type()
        empty_cells, fish_cells  = self.my_grid.check_possible_moves(x, y)
        moved = False
        dx = 0
        dy = 0

        match entity_type:
            case "fish":
                if(empty_cells):
                    dx, dy = random.choice(empty_cells)
                    can_reproduce_fish = entity.reproduce(self.turn) 
                    if can_reproduce_fish :  
                        new_id = max(self.fish_dict.keys(), default=-1) + 1
                        self.fish_dict[new_id] = Fish(x, y)
                    else:
                        self.my_grid.affect_entity(x, y, "empty")
                    moved = True
            case "shark":
                if fish_cells:                    
                    dx, dy = random.choice(fish_cells)
                    # Calcul de la position du poisson à manger (avec wrapping)
                    target_x = (x + dx) % self.grid_size
                    target_y = (y + dy) % self.grid_size
                    # Trouver et supprimer le poisson du dictionnaire
                    entity.eat_fish(target_x, target_y, self.fish_dict.items(),  self.fish_dict)
                    moved = True
                    self.my_grid.affect_entity(x, y, "empty")
                    entity.decrease_stamina()
                elif(empty_cells):
                    dx, dy = random.choice(empty_cells)
                    shark_can_reproduce = entity.reproduce(self.turn)
                    if shark_can_reproduce :
                        new_id = max(self.shark_dict.keys(), default=-1) + 1
                        self.shark_dict[new_id] = Shark(x, y) 
                    else:
                        self.my_grid.affect_entity(x, y, "empty")
                    entity.decrease_stamina()
                    moved = True
                else:
                    entity.decrease_stamina()
               
                if entity.get_stamina() <= 0:
                    entity.remove_shark(self.shark_dict, entity_id)
                    current_x = (x + dx) % self.grid_size if moved else x
                    current_y = (y + dy) % self.grid_size if moved else y
                    self.my_grid.affect_entity(current_x, current_y, "empty")
                    return
                
        if (moved == True ):
            # Updating positions with wrapping
            x = (x + dx) % self.grid_size
            y = (y + dy) % self.grid_size
            entity.x = x    #update  in dictonary the entity position
            entity.y = y
            self.my_grid.affect_entity(x, y, entity_type)
            return(x, y)
        

grid_size = 10
my_grid = Grid(grid_size)
w = World(my_grid, grid_size)



while w.turn < 0:
    #os.system('clear') 
    w.turn += 1
    print(f"--- Tour {w.turn} ---")
    w.move_entities()
    time.sleep(0.5)
from interface import launch_interface

if __name__ == "__main__":
    my_world_grid = Grid(15) 
    launch_interface(my_world_grid)
