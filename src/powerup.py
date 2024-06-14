import pygame
import random
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/rainbow_car.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = random.randint(ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER)
        self.posY = random.randint(0, 800) * -1
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.speed = 5

    def update(self):
        self.posY += self.speed
        self.rect.center = [self.posX, self.posY]
