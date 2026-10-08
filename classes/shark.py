"""This is the dedicated file to the Shark Class.
This file inherits from Fish class"""

from fish import Fish


class Shark (Fish):
    def __init__ (self, x: int, y: int):
        self.x = x
        self.y = y
        self.reproduction_time = 12
        self.turn = 0
        self.time_remaining = 16

    def shark_eating(self,turn,fish):
        if self.x and self.y == fish.x and fish.y:
            self.time_remaining += 7
        del fish    

    def shark_starvation_time(self,turn):
        if self.time_remaining == 0:
                del shark
    
