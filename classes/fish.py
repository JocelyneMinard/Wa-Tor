'''Fish class for Wa-Tor simulation
manage fish entity and its behavior'''

class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = 8
        self.age = 0

    def __str__(self) -> str:
        return str(self.x) + ": " + str(self.y)


    # reproduce method to move the fish and leave a baby behind at the old position
    def reproduce(self, world_turn: int) -> bool:
        # Check if the current world turn is a multiple of 8
        self.age += 1
        if (self.age >= self.reproduction_time) and (world_turn > 0) :
            self.age = 0
            return True
        return False 

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_type(self) -> str:
        return "fish"

    def remove_fish(self, fish_dict: dict, fish_id: int) -> None:
        """delete the entity from the dictionary if it exists"""
        if fish_id in fish_dict:
            del fish_dict[fish_id]

