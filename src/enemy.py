import pygame
import random
from observerp import Subscriber
from strategy import ZigZagMovement, StillMovement
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type):
        if enemy_type == "Yellow":
            return Enemy(StillMovement(), "src/images/yellow_car.png")
        elif enemy_type == "Blue":
            return Enemy(ZigZagMovement(), "src/images/blue_car.png")
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")


class Enemy(Subscriber, pygame.sprite.Sprite):
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
        # reviso que speed no sea tipo None
        if speed is None:
            raise ValueError("Speed cannot be None")
        self.speed = speed
        self.movement_strategy.move(self)

    def updateSub(self):
        self.movement_strategy = StillMovement()
        self.movement_strategy.move(self)
