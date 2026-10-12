# This file manages the simulation grid
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

    def affect_entity(self, x, y, entity_type):
        if entity_type == "fish":
            self.grid[y][x] = self.style_fish
        elif entity_type == "shark":
            self.grid[y][x] = self.style_shark
        else:
            self.grid[y][x] = self.style_sea

    def check_cell(self, x, y):
        return self.grid[y][x] 
    
    def check_possible_moves(self, x, y):
        # 1. Liste des directions de déplacement (dx, dy)
        possible_moves = [
            (-1, 0),  # Gauche
            (1, 0),   # Droite
            (0, -1),  # Haut
            (0, 1)    # Bas
        ]

        empty_cells = []
        fish_cells = []
        shark_cells = []

        # 2. On parcourt chaque déplacement possible
        for dx, dy in possible_moves:
            # Calcul des coordonnées voisines avec wrapping
            # Attention : Ton code utilise self.grid[y][x], donc nx correspond à l'axe X (largeur) et ny à l'axe Y (hauteur)
            nx = (x + dx) % self.size
            ny = (y + dy) % self.size
            
            # 3. Récupération du contenu de la case
            cell_content = self.grid[ny][nx]
            
            # 4. Tri en stockant le déplacement relatif (dx, dy)
            if cell_content == self.style_sea:
                empty_cells.append((dx, dy))
            elif cell_content == self.style_fish:
                fish_cells.append((dx, dy))
            #elif cell_content == self.style_shark:
                #shark_cells.append((dx, dy))
            
        return empty_cells, fish_cells

    def check_grid(self):
        # Conserver uniquement le print principal si nécessaire pour le debug
        print("Vérification de la grille et recherche des cases vides.")
        
        # Compréhension de liste imbriquée pour extraire les coordonnées (x, y)
        my_grid_empty_cells = [
            (x, y) 
            for y, row in enumerate(self.grid) 
            for x, cell in enumerate(row) 
            if cell == self.style_sea
        ]

        print(my_grid_empty_cells)
        return my_grid_empty_cells


# Zone de test
if __name__ == "__main__":
    my_grid = Grid(10)
    my_grid.affect_entity(0, 0, "fish")
    my_grid.affect_entity(1, 0, "fish")
    my_grid.display()
    
    empty, fish = my_grid.check_possible_moves(0, 0)
    print(f"Cases vides autour de (0,0) : {empty}")
    print(f"Poissons autour de (0,0) : {fish}")
    my_grid.check_grid()