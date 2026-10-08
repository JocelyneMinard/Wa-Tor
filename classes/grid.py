# This file manage simlation grid

class Grid:
    def __init__(self, size: int) -> None:
        self.size = size
        self.init_grid()

    def init_grid(self):
        self.grid = [["\033[96m██\033[0m" for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        for row in self.grid:
            print("".join(row))

    def affect_entity(self,x, y, type):
        if (type =="fish"):
            self.grid[x][y] = "\033[96m🐟\033[0m"
        elif(type == "shark"):
            self.grid[x][y] = "\033[96m🦈\033[0m"
        else:
            print("Fish or Shark idiot!!")

            
    def check_cells(self, x, y):
        pass

if __name__ == "main":
    my_grid = Grid(20)
    my_grid.display()
