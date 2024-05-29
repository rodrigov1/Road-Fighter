import random
from abc import abstractmethod
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER

class MovementStrategy:
    @abstractmethod
    def move(self, enemy):
        raise NotImplementedError("This method should be overridden by subclasses")

# TODO: Still not implemented the blue car which uses random movement
class RandomMovement(MovementStrategy):
    def move(self, enemy):
        enemy.rect.y += enemy.speed
        # Check if the enemy is within the road boundaries for random movement
        if ROAD_LEFT_BORDER <= enemy.rect.x <= ROAD_RIGHT_BORDER:
            enemy.rect.x += random.randint(-enemy.speed, enemy.speed)

class StillMovement(MovementStrategy):
    def move(self, enemy):
        enemy.posY += enemy.speed
        enemy.rect.center = [enemy.posX, enemy.posY]
