import grid

class Fish:
    def __init__(self, x: int, y: int, reproduction_time: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = reproduction_time
        self.age = 0
      

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    
