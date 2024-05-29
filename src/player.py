import pygame
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER

class Player(pygame.sprite.Sprite):
    def __init__(self, posX, posY, speed):
        super().__init__()
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.speed = speed
        self.rect.center = [self.posX, self.posY]

    def update(self, direction):
        if direction == "right":
            if self.posX < ROAD_RIGHT_BORDER:
                self.posX += self.speed

        if direction == "left":
            if self.posX > ROAD_LEFT_BORDER:
                self.posX -= self.speed

        self.rect.center = [self.posX, self.posY]
