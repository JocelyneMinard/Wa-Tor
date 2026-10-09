# This file manages simlation grid
import random

class Grid:
    def __init__(self, size: int) -> None:
        self.size = size
        self.style_sea = "\033[96m██\033[0m"
        self.style_fish = "\033[96m🐟\033[0m"
        self.style_shark = "\033[96m🦈\033[0m"
        self.init_grid()

    def init_grid(self):
        self.grid = [[self.style_sea for _ in range(self.size)] for _ in range(self.size)]

    def display(self):
        for row in self.grid:
            print("".join(row))

    def affect_entity(self,x, y, type):
        if (type =="fish"):
            self.grid[x][y] = self.style_fish
        elif(type == "shark"):
            self.grid[x][y] = self.style_shark
        else:
            self.grid[x][y] = self.style_sea

            
    def check_cells(self, x, y):
        # Verifying neighbouring cells
        adjacent_cells = [
            (1,1),
            (1,-1),
            (-1,1),
            (-1,-1),
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
            #((x - 1) % self.size, y),  # Up
            #((x + 1) % self.size, y),  # Down
            #(x, (y - 1) % self.size),  # Left
            #(x, (y + 1) % self.size)   # Right
        ]
        
        empty_cells = []
        for cell in adjacent_cells:
            if self.grid[cell[0]][cell[1]] == self.style_sea:
                empty_cells.append(cell)

        occupied_cells = [cell for cell in adjacent_cells if self.grid[cell[0]][cell[1]] != self.style_sea]
        #This function verifies if the neibouring cases are blocked
        fish_cells = [cell for cell in adjacent_cells if self.grid[cell[0]][cell[1]] == self.style_fish]

        return empty_cells, occupied_cells, fish_cells

    def move(self, x,y):
        empty_cells, occupied_cells, fish_cells  = self.check_cells(x, y)
        if(empty_cells != ""):
            dx, dy = random.choice(empty_cells)
        self.affect_entity(x,y, "empty")
        # Updating positions with wrapping
        x = (x + dx) % self.size
        y = (y + dy) % self.size
        return(x, y)
    
        
if __name__ == "main":
    my_grid = Grid(20)
    my_grid.display()
