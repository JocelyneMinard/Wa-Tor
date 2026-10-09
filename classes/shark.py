"""This is the dedicated file to the Shark Class.
This file inherits from Fish class"""

from fish import Fish

#1 Inherit from Fish classe
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
#3 Define eating 
    def shark_eating(self,turn,fish):
        if self.x and self.y == fish.x and fish.y:
            self.time_remaining = turn + 7
            del fish    
#4 Define shark's death
    def shark_starvation_time(self,turn,shark):
        if turn >= self.time_remaining:
            del shark
#5 Define shark's position on the grid   
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
#6 Define shark's type   
    def get_type(self):
        return "shark"

        
         
