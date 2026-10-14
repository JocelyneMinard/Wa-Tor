'''Fish class for Wa-Tor simulation
manage fish entity and its behavior'''

class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.age = 0
        self.reproduction_time = 8
        
    def __str__(self) -> str:
        return str(self.x) + ": " + str(self.y)

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_type(self) -> str:
        return "fish"

    # reproduce method to move the fish and leave a baby behind at the old position
    def reproduce(self, world_turn: int) -> bool:
        # Check if the current world turn is a multiple of 8
        self.age += 1
        if (self.age >= self.reproduction_time) and (world_turn > 0) :
            self.age = 0
            return True
        return False 

    # Dying 
    def remove_entity(self, entity_dict: dict, entity_id: int) -> None:
        """delete the entity from the dictionary if it exists"""
        if entity_id in entity_dict:
            del entity_dict[entity_id]
