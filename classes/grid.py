# This file manage simlation grid

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
        if (x -1, y -1):
            pass
        

    def move(self, x,y):
        # Déplacement (par exemple, on avance d'une case vers la droite)
        dx = 1
        dy = 0
        self.affect_entity(x,y, "empty")
        # Mise à jour avec "wrapping" (enroulement)
        x = (x + dx) % self.size
        y = (y + dy) % self.size
        
        return(x, y)


if __name__ == "main":
    my_grid = Grid(20)
    my_grid.display()
