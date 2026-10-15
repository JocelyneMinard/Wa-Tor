from classes.grid import Grid 
from classes.world import World 
import os, time
import configparser

# Création de l'objet et lecture du fichier
config = configparser.ConfigParser()
config.read('config.ini')

# put color for emoji because .ini interpret var on brut text
style_sea = f"\033[96m{config['GRID']['style_sea']}\033[0m"
style_fish = f"\033[96m\033[106m{config['GRID']['style_fish']}\033[0m"
style_shark = f"\033[96m\033[106m{config['GRID']['style_shark']}\033[0m"

my_grid = Grid(   
    int(config['DEFAULT']["grid_size"]), 
    style_sea = style_sea, 
    style_fish = style_fish, 
    style_shark = style_shark
)

w = World(
    my_grid, 
    int(config['DEFAULT']["grid_size"]), 
    int(config['DEFAULT']["population_init_fish"]), 
    int(config['DEFAULT']["population_init_shark"])
)


while True:
    os.system('clear') 
    w.turn += 1
    w.move_entities()
    print(f"--------------Turn : {w.turn}--------------")
    print(f"Fish number : {len(w.fish_dict)}")
    print(f"Shark number : {len(w.shark_dict)}")
    time.sleep(0.7)
