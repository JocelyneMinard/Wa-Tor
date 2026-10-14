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
    
    def eat_fish(self, target_x, target_y, item, fish_dict):
        for fid, fobj in list(item):
            if fobj.get_x() == target_x and fobj.get_y() == target_y:
                fobj.remove_entity(fish_dict, fid)
                self.increase_stamina()
                break
    
    def get_stamina(self) :
        #replenish stamina
        return self.stamina

    def increase_stamina(self):
        #replenish stamina
        self.stamina == min(self.stamina + 7, self.original_stamina)

    # Decreases stamina
    def decrease_stamina(self):
        self.stamina -= 1       
