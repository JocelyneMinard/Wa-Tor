# This class manages the simulation

from classes.fish import Fish
from classes.shark import Shark
import random

class World:
    def __init__(self, my_grid, grid_size: int, fish_number, shark_number) -> None:
        self.population_init_fish = fish_number
        self.population_init_shark = shark_number
        self.my_grid = my_grid  
        self.grid_size = grid_size
        self.fish_dict = {}
        self.shark_dict = {}
        self.turn = 0
        my_grid_empty_cells = my_grid.check_grid()

        if int(self.population_init_fish * 0.5) >= (self.grid_size * self.grid_size):
            self.population_init_fish = int((self.grid_size * self.grid_size) * 0.5)
        for i in range(self.population_init_fish):
            if my_grid_empty_cells:
                x, y = random.choice(my_grid_empty_cells)
                my_grid_empty_cells.remove((x, y))  # This removes doubles from cells
                self.my_grid.affect_entity(x, y, "fish")
                self.fish_dict[i] = Fish(x, y)

        # Filling grid with sharks
        if int(self.population_init_shark * 0.3) >= (self.grid_size * self.grid_size):
            self.population_init_shark = int((self.grid_size * self.grid_size) * 0.3)
        for i in range(self.population_init_shark):
            if my_grid_empty_cells:
                x, y = random.choice(my_grid_empty_cells)
                my_grid_empty_cells.remove((x, y))  # Removing last cell
                self.my_grid.affect_entity(x, y, "shark")
                self.shark_dict[i] = Shark(x, y)
        my_grid.display()


    # mouvement fish and shark
    def move_entities(self) -> None:
        # fix list of dict shark
        for entity_id in list(self.shark_dict.keys()):
            if entity_id in self.shark_dict:
                self.move(self.shark_dict[entity_id], entity_id)
                
        # fix list of dict fish
        for entity_id in list(self.fish_dict.keys()):
             if entity_id in self.fish_dict:
                self.move(self.fish_dict[entity_id], entity_id)
        self.my_grid.display()

    def move(self, entity, entity_id: int):
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
                    # Calculating predetion system, necessary for the shark to eat
                    target_x = (x + dx) % self.grid_size
                    target_y = (y + dy) % self.grid_size
                    # Find and delete fish from position
                    for fid, fobj in list(self.fish_dict.items()):
                        if fobj.get_x() == target_x and fobj.get_y() == target_y:
                            del self.fish_dict[fid]
                    entity.eat()
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
                    # delete shark
                    del self.shark_dict[entity_id]
                    # remove cell when shark just move or origin cell if don' move
                    if moved:
                        current_x = (x + dx) % self.grid_size
                        current_y = (y + dy) % self.grid_size
                        self.my_grid.affect_entity(current_x, current_y, "empty")
                    else:
                        self.my_grid.affect_entity(x, y, "empty")
                    return
                
        if (moved == True ):
            # Updating positions with wrapping
            new_x = (x + dx) % self.grid_size
            new_y = (y + dy) % self.grid_size
            #Update  in dictonary the entity position
            entity.set_position(new_x, new_y)
            self.my_grid.affect_entity(new_x, new_y, entity_type)
            return (new_x, new_y)

