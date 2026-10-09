# This class manage the simulation
from grid import Grid 
from fish import Fish
from shark import Shark
import random

class World:
    def __init__(self, my_grid, grid_size) -> None:
        self.population_init_fish = 5
        self.population_init_shark = 1
        self.grid_size = grid_size
        self.fish_dict = {}
        self.shark_dict = {}

        for i in range(self.population_init_fish) :
            x = random.randint(0, self.grid_size -1)
            y = random.randint(0, self.grid_size -1)
            my_grid.affect_entity(x,y, "fish")
            self.fish_dict[i] = Fish(x,y)

        for i in range(self.population_init_shark) :
            x = random.randint(0, self.grid_size -1)
            y = random.randint(0, self.grid_size -1)
            my_grid.affect_entity(x,y, "shark")
            self.shark_dict[i] = Shark(x,y)

        @property
        def fish_dict(self):
            return self.fish_dict

        @property
        def shark_dict(self):
            return self.shark_dict

        my_grid.display()
        
    # mouvement fish and shark
    def move_entities(self, my_grid):
        # for fish
        for fish in self.fish_dict.items():
            ancien_x, ancien_y = fish.x, fish.y
            new_x = (ancien_x + random.choice([-1, 0, 1])) % self.grid_size
            new_y = (ancien_y + random.choice([-1, 0, 1])) % self.grid_size
            self.my_grid.affect_entity(ancien_x, ancien_y, "empty") 
            self.my_grid.affect_entity(new_x, new_y, "fish") 
            fish.x = new_x
            fish.y = new_y
            
            #for shark
        for shark in self.shark_dict.items():
            ancien_x, ancien_y = shark.x, shark.y
            new_x = (ancien_x + random.choice([-1, 0, 1])) % self.grid_size
            new_y = (ancien_y + random.choice([-1, 0, 1])) % self.grid_size
            
            self.my_grid.affect_entity(ancien_x, ancien_y, "empty")
            self.my_grid.affect_entity(new_x, new_y, "shark")
            
            shark.x = new_x
            shark.y = new_y
        
        my_grid.display()

my_grid = Grid(20)
w = World(my_grid, 20)

print(w.fish_dict)
print(w.shark.dict)