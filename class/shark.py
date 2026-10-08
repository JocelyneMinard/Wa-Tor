import Fish
import grid

class Shark(Fish):
    def __init__ (self, x: int, y: int, reproduction_time: int, starvation_time: int):
        self.x = x
        self.y = y
        self.reproduction_time = reproduction_time
        self.age = 0