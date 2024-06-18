import pygame
import random
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER


class PowerUpFactory:
    @staticmethod
    def create_powerup(powerup_type):
        match powerup_type:
            case "Blue":
                return PowerUp("images/blue_truck.png", "Blue")
            case "Pink":
                return PowerUp("images/pink_truck.png", "Pink")
            case _:
                raise ValueError(f"Unknown powerup type: {powerup_type}")


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image_path, type):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = random.randint(ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER)
        self.posY = random.randint(0, 800) * -1
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.speed = 5
        self.type = type

    def update(self):
        self.posY += self.speed
        self.rect.center = (self.posX, self.posY)
