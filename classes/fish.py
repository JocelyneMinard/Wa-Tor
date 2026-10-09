'''fish class for Wa-Tor simulation
manage fish entity and its behavior'''

class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = 8  # Default reproduction time
        self.turn = 0

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def reproduce(self) -> bool:
        self.turn += 1
        if self.turn >= self.reproduction_time:
            self.turn = 0
            return True
        return False
    def get_x(self) -> int:
        return self.x
    
    def get_y(self) -> int:
        return self.y