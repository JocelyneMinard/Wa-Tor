# This file manage simlation grid
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
        # Vérification des cellules adjacentes (haut, bas, gauche, droite)
        adjacent_cells = [
            ((x - 1) % self.size, y),  # Haut
            ((x + 1) % self.size, y),  # Bas
            (x, (y - 1) % self.size),  # Gauche
            (x, (y + 1) % self.size)   # Droite
        ]
        
        empty_cells = []
        for cell in adjacent_cells:
            if self.grid[cell[0]][cell[1]] == self.style_sea:
                empty_cells.append(cell)
        occupied_cells = [cell for cell in adjacent_cells if self.grid[cell[0]][cell[1]] != self.style_sea]
        return empty_cells, occupied_cells

    def move(self, x,y):

        self.affect_entity(x,y, "empty")
        # Déplacement (par exemple, on avance d'une case vers la droite)
        dx = random.randint(-1,1)
        dy = random.randint(-1,1)
        # Mise à jour avec "wrapping" (enroulement)
        x = (x + dx) % self.size
        y = (y + dy) % self.size
        
        return(x, y)


if __name__ == "main":
    my_grid = Grid(20)
    my_grid.display()
