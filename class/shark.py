import Fish
import grid

class Shark(Fish):
    def __init__ (self, x: int, y: int):
        self.x = x
        self.y = y
        self.reproduction_time = 12
        self.age = 0