import pygame
import random
from strategy import StillMovement
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type):
        if enemy_type == "Yellow":
            return Enemy(StillMovement(), "../images/yellow_enemy.png")
        # elif enemy_type == "Blue":
        #     return Enemy(RandomMovement(), "../images/blue_enemy.png")
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, movement_strategy, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = random.randint(ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER)
        self.posY = random.randint(0, 800) * -1
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.movement_strategy = movement_strategy
        self.speed = 0

    def update(self, speed):
        self.speed = speed
        self.movement_strategy.move(self)
