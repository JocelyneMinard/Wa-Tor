# This file manage simlation grid

class Grid:
    def __init__(self, size: int) -> None:
        self.size = size

    def display(self):
        grid = []
        for i in range(self.size):
            grid.append(["\033[96m███\033[0m"] * self.size)

        for row in grid:
            print("".join(row))


my_grid = Grid(20)
my_grid.display()
