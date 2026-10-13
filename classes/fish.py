'''fish class for Wa-Tor simulation
manage fish entity and its behavior'''


class Fish:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = 8
        self.turn = 0

    def __str__(self):
        return str(self.x) + ": " + str(self.y)

    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


          # reproduce method to move the fish and leave a baby behind at the old position
    def reproduce(self, nx: int, ny: int, world_turn: int):
        # 1. Save the old coordinates for the baby
        old_x = self.x
        old_y = self.y
        
        # 2. Move the parent fish to the new cell (happens anyway)
        self.x = nx
        self.y = ny
        
        # 3. Check if the current world turn is a multiple of 8
        if world_turn > 0 and world_turn % 8 == 0:
            self.age = world_turn  # Updates the age with the current turn
            
            # Create and return the new baby at the old cell
            return Fish(old_x, old_y)
            
        # If it cannot reproduce, the parent has still moved, but returns None
        return None




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

    