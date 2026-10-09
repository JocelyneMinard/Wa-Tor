"""This is the dedicated file to the Shark Class.
This file inherits from Fish class"""

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
#2 Reproduction time
    def reproduce_shark(self) -> bool:
            if self.turn >= self.reproduction_time:
                self.turn = 0
                return True
            return False
#3 Define eating(increases the number of turns left before dying)
    def shark_eating(self,turn,fish):
        if self.x == fish.x and self.y == fish.y:
            self.time_remaining = turn + 7
            return True  
#4 Define shark's death
    def shark_starvation_time(self,turn,shark):
        if turn >= self.time_remaining:
            return False
#5 Define shark's position on the grid   
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
#6 Define shark's type   
    def get_type(self):
        return "shark"

        
         
