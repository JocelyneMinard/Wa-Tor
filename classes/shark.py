"""This is the dedicated file to the Shark Class.
This file inherits from Fish class"""

import random
from fish import Fish

#1 Inherits from Fish class
class Shark (Fish):
    def __init__ (self, x: int, y: int):
        self.x = x
        self.y = y
        self.reproduction_time = 12
        self.turn = 0
        self.time_remaining = 16
        self.turn += 1

    def __str__(self):
        return str(self.x) + ": " + str(self.y)

#2 Reproduction time
    def reproduce_shark(self,world_turn):
        if world_turn > 0 and world_turn % 12 == 0:
            self.age = world_turn 
            return Shark()
        return None 


#3 Integrated Move & Eat Logic
    def move_and_eat(self, grid_size, fish_cells, empty_cells) -> str:
        """
        Implementation of the moving and the eating system.
        Returns eat an move actions.
        """
        #Increases age each turn
        self.turn += 1
        
        # 
        if fish_cells:
            dx, dy = random.choice(fish_cells)
            self.x = (self.x + dx) % grid_size
            self.y = (self.y + dy) % grid_size
            
            # Stamina bonus when eating
            self.time_remaining += 7 
            return "eat"
            
        # Second case: when no fishes in zone of interest, move in empty cases
        elif empty_cells:
            dx, dy = random.choice(empty_cells)
            self.x = (self.x + dx) % grid_size
            self.y = (self.y + dy) % grid_size
            
            # Loose 1 stamina every turn
            self.time_remaining -= 1
            return "move"
            
        # 5 : Shark is blocked
        else:
            self.time_remaining -= 1
            return "stay"

#6 Define shark's death
    def shark_starvation_time(self, turn, shark):
        if turn >= self.time_remaining:
            return False
            
#7 Define shark's position on the grid   
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y

#8 Define shark's type   
    def get_type(self):
        return "shark"
