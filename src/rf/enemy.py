from email.mime import image
import pygame
import random
from rf.observerp import Subscriber
from rf.strategy import ZigZagMovement, StillMovement
from rf.screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER
from rf.images import (
    yellow_car,
    blue_car,
    rainbow_car,
    frozen_bluecar,
    frozen_yellowcar,
    limitless_bluecar,
    limitless_yellowcar,
)


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type):
        match enemy_type:
            case "Yellow":
                return Enemy(StillMovement(), yellow_car, "Yellow")
            case "Blue":
                return Enemy(ZigZagMovement(), blue_car, "Blue")
            case "Rainbow":
                return Enemy(ZigZagMovement(), rainbow_car, "Rainbow")
            case _:
                raise ValueError(f"Unknown enemy type: {enemy_type}")


class Enemy(Subscriber, pygame.sprite.Sprite):
    def __init__(self, movement_strategy, image_path, type):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = random.randint(ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER)
        self.posY = random.randint(0, 800) * -1
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.movement_strategy = movement_strategy
        self.speed = 0
        self.type = type

    def update(self, speed):
        # reviso que speed no sea tipo None
        if speed is None:
            raise ValueError("Speed cannot be None")

        self.speed = speed
        self.movement_strategy.move(self)

    def updateSub(self, powerup):
        match powerup:
            case "Frozen":
                self.movement_strategy = StillMovement()
            case "Limitless":
                self.movement_strategy = ZigZagMovement()
            case "Reset":
                if self.type == "Blue":
                    self.movement_strategy = ZigZagMovement()
                else:
                    self.movement_strategy = StillMovement()
            case _:
                pass

        image_path = yellow_car
        if powerup == "Reset":
            if self.type == "Blue":
                image_path = blue_car
        else:
            powerup_name = str(powerup).lower()
            match powerup_name:
                case "frozen":
                    if self.type == "Blue":
                        image_path = frozen_bluecar
                    else:
                        image_path = frozen_yellowcar
                case "limitless":
                    if self.type == "Blue":
                        image_path = limitless_bluecar
                    else:
                        image_path = limitless_yellowcar

        self.image = pygame.image.load(image_path).convert_alpha()
