"""This is the dedicated file to the Shark Class.
This file inherits from Fish class"""

from classes.fish import Fish

#1 Inherits from Fish class
class Shark (Fish):
    def __init__ (self, x: int, y: int):
        self.x = x
        self.y = y
        self.reproduction_time = 12
        self.stamina = 16
        self.age = 0

    def __str__(self):
        return str(self.x) + ": " + str(self.y)

    # Return shark's position on the grid   
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    # Return shark's type   
    def get_type(self):
        return "shark"
    
    def eat_fish(self, target_x, target_y, item, fish_dict):
        for fid, fobj in list(item):
            if fobj.get_x() == target_x and fobj.get_y() == target_y:
                Fish.remove_fish(self, fish_dict, fid)
                break
        self.increase_stamina()
    
    def get_stamina(self) :
        #replenish stamina
        return self.stamina

    def increase_stamina(self):
        #replenish stamina
        self.stamina += 7

    # Decreases stamina
    def decrease_stamina(self):
        self.stamina -= 1       

    # Dying shark
    def remove_shark(self, shark_dict: dict, shark_id) -> None:
        """Removes shark when dying """
        if shark_id in shark_dict:
            del shark_dict[shark_id]
