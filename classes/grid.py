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
            self.grid[y][x] = self.style_fish
        elif(type == "shark"):
            self.grid[y][x] = self.style_shark
        else:
            self.grid[y][x] = self.style_sea

    def check_cell(self, x, y):
        return self.grid[y][x] 
    
    def check_cells(self, x, y):
        # Verifying neighbouring cells
        possible_cells = [
            (-1,0),
            (1,0),
            (0,-1),
            (0,1)
        ]

        adjacent_cells = []

        for cells in possible_cells:
            adjacent_cells.append((x+cells[0], y + cells[1]))

        empty_cells = []
        fish_cells = []
        shark_cells = []
        for cell in adjacent_cells:
            if self.grid[cell[1]][cell[0]] == self.style_sea:
                empty_cells.append(cell)
            elif self.grid[cell[1]][cell[0]] == self.style_fish:
                fish_cells.append(cell)
            else:
                shark_cells.append(cell)
            
        return empty_cells, fish_cells, shark_cells

    def check_grid(self):
        my_grid_empty_cells = []
        coords = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == self.style_sea:
                    my_grid_empty_cells.append(cell)
                    coords.append((x, y))

                print(f"{'x':>4} | {'y':>4}")
                print("-" * 11)
                for x, y in coords:
                    print(f"{x:>4} | {y:>4}")

        return my_grid_empty_cells

        
if __name__ == "main":
    my_grid = Grid(20)
    my_grid.display()

my_grid = Grid(20)
my_grid.display()
print(my_grid.check_grid())
