''' Class for manage fish in grid 
 a fish, at each time step :
 get older,
 moves to a neighboring cell if it is empty,
    reproduces if it is old enough, and leaving a baby behind
'''
import grid

class Fish:
    def __init__(self, x: int, y: int, reproduction_time: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time: int = 8
        self.age: int = 0
        
    
    def new_born(self) -> Fish:
        ''' Create a new fish with the same reproduction time as the parent '''
        return Fish(self.x, self.y, self.reproduction_time)
    
    def turn(
        self,
        grid: grid,
        x: int,
        y: int,
        age: int,
     )      -> None:   
        # step 1: reproduce if possible
        if self.age >= self.reproduction_time:
            self.age = 8
            baby = self.new_born()
            
            #the baby does not act during this time step
            baby.age = 0
            grid[y][x] = baby
    
            
