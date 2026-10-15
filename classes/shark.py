"""This is the dedicated file to the Shark Class.
This file inherits from Fish class"""

from classes.fish import Fish

#1 Inherits from Fish class
class Shark(Fish):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)  # x, y, age from Fish
        self.reproduction_time = 12
        self.original_stamina = 16
        self.stamina = 16

    # Return shark's type   
    def get_type(self):
        return "shark"
    
    def eat(self):
        self.increase_stamina()
    
    def get_stamina(self) :
        #replenish stamina
        return self.stamina

    def increase_stamina(self):
        #replenish stamina
        self.stamina = min(self.stamina + 7, self.original_stamina)

    # Decreases stamina
    def decrease_stamina(self):
        self.stamina -= 1       
