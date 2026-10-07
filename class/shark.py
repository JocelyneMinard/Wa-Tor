import fish
class Shark (Fish):
    def __init__(self, x: int, y: int, reproduction_time: int, eat) -> None:
        self.x = x
        self.y = y
        self.reproduction_time = reproduction_time 
        self.eat = eat

    def eat (self.eat):
        from fish import fish  # Assurez-vous que le nom de la classe dans votre module est correct (souvent majuscule)

    def predation(sharks: list[Shark], fishes: list[Fish]) -> None:
        """
        Vérifie les coordonnées de chaque requin et supprime les poissons
        qui se trouvent exactement sur la même case (mêmes coordonnées x et y).
     """
        # 1. Stocker les coordonnées des requins dans un ensemble (set) de tuples (x, y).
        positions_requins = {(shark.x, shark.y) for shark in sharks}
    
    # 2. On filtre la liste des poissons pour ne garder que ceux qui ne croisent aucun requin.
    # On reconstruit la liste pour éviter les bugs liés à la suppression d'éléments pendant une boucle.
        fishes_remaining = [fish for fish in fishes if (fish.x, fish.y) not in positions_requins]
    def prepare_turn(self)