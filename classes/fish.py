'''fish class for Wa-Tor simulation
manage fish entity and its behavior'''

class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = 8  # Default reproduction time
        self.turn = 0

    #move method to update the position of the fish
    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # reproduce method to check if the fish can reproduce
    def reproduce(self) -> bool:
        self.turn += 1
        if self.turn >= self.reproduction_time:
            self.turn = 0
            return True
        return False
    
    # get_x method to return the x coordinate of the fish
    def get_x(self) -> int:
        return self.x
    
    # get_y method to return the y coordinate of the fish
    def get_y(self) -> int:
        return self.y
    
    # get_type method to return the type of the entity
    def get_type(self) -> str:
        return "fish"

    def remove_fish(self, fish_dict: dict, fish_id: int) -> None:
        """delete the entity from the dictionary if it exists"""
        if fish_id in fish_dict:
            del fish_dict[fish_id]  # really removes the fish from the dictionary
