import random
from abc import abstractmethod
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER

class MovementStrategy:
    @abstractmethod
    def move(self, enemy):
        raise NotImplementedError("This method should be overridden by subclasses")

class StillMovement(MovementStrategy):
    def move(self, enemy):
        enemy.posY += enemy.speed
        enemy.rect.center = [enemy.posX, enemy.posY]
        
class ZigZagMovement(MovementStrategy):
    aux = random.choice([True, False])
    
    def move(self, enemy):
        enemy.posY += enemy.speed
        
        if self.aux and enemy.posX + 2 < ROAD_RIGHT_BORDER:
            self.aux = True
            enemy.posX += 2
        elif not self.aux and enemy.posX - 2 > ROAD_LEFT_BORDER:
            self.aux = False
            enemy.posX -= 2
        else:
            self.aux = not self.aux
            
        enemy.rect.center = [enemy.posX, enemy.posY]
