# This file manage simlation grid

class Grid:
    def __init__(self, size: int) -> None:
        self.size = size

    def display(self):
        grid = []
        for i in range(self.size):
            grid.append(["\033[96m██\033[0m"] * self.size)
        
        #grid[15][15] = "\033[96m🐟\033[0m"
        grid[15][15] = "\033[1m\033[91m\033[106m⋟ \033[0m"

        grid[12][12] = "\033[1;37;106m⪦ \033[0m"

        for row in grid:
            print("".join(row))


    def neighbor():
        pass

my_grid = Grid(20)
# les requin et les poisson vont devoir aussi prendre le paramètre de taille pour ne pas sortir de la grille et créer une erreur out of range
my_grid.display()
