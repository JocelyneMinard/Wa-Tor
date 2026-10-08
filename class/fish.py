'''fish class for Wa-Tor simulation
manage fish entity and its behavior'''

import grid

class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = 8  # Default reproduction time
        self.age = 0
      

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def reproduce(self) -> bool:
        self.age += 1
        if self.age >= self.reproduction_time:
            self.age = 0
            return True
        return False
    