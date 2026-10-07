''' Class for manage fish in grid 
 a fish, at each time step :
 get older,
 moves to a neighboring cell if it is empty,
    reproduces if it is old enough, and leaving a baby behind
'''
from __future__ import annotations
import random
from typing import TYPE_CHECKING, Optional as optional
import config

if TYPE_CHECKING:
    from planet import planet

class Fish:
    def __init__(self, x: int, y: int, reproduction_time: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = reproduction_time
        self.age: int = 4
        self.last_step: int = 0
        
    def prepare_turn(self) -> None:
        self.age -= 1
    
    def is_alive(self) -> bool:
        return self.alive 
    
    def kill(self) -> None:
        self.alive = False
    
    def choose_destination(
        self,
        planet: planet,
        x: int,
        y: int
    ) -> optional[tuple[int, int]]:
        empty_cells = planet.get_empty_neighbors(x, y)
        return empty_cells[0] if empty_cells else None
    
    def eat(self, planet: planet, x: int, y: int) -> None:
        pass
    
    def new_born(self) -> Fish:
        ''' Create a new fish with the same reproduction time as the parent '''
        return Fish(self.x, self.y, self.reproduction_time)
    
    def turn(
        self,
        planet: planet,
        x: int,
        y: int,
        step: int,
     )      -> None:
        '''plays a complete turn : age, die, move, eat, and reproduce if possible'''
        if not self.is_alive():
            return
    # step 1: the animal acts and gets older
        self.last_step = step
        self.prepare_turn()
        
    # step 2: choose a destination 
        destination = self.choose_destination(planet, x, y)
        if destination is None:
            return
        
        # step 3: eat, then move 
        nx, ny = destination
        self.eat(planet, nx, ny)
        planet.move_animal(x, y, nx, ny)
        
        # step 4: reproduce if possible
        if self.age >= self.reproduction_time:
            self.age = 4
            baby = self.new_born()
            
            #the baby does not act during this time step
            baby.last_step = step
            planet.grid[y][x] = baby
    
            
