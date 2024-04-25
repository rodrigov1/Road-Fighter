import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/car_enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.choice((248,332,420,500))
        self.rect.y = -100
        self.speed = random.choice((3, 4, 5, 6, 7, 8))

    def update(self):
        self.rect.y += self.speed