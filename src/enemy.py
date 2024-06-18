from email.mime import image
import pygame
import random
from observerp import Subscriber
from strategy import ZigZagMovement, StillMovement
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type):
        match enemy_type:
            case "Yellow":
                return Enemy(StillMovement(), "../images/yellow_car.png", "Yellow")
            case "Blue":
                return Enemy(ZigZagMovement(), "../images/blue_car.png", "Blue")
            case "Rainbow":
                return Enemy(ZigZagMovement(), "../images/rainbow_car.png", "Rainbow")
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
        
        car_path = str(self.type).lower() + "_car.png"
        
        if powerup == "Reset":
            image_path = "../images/" + car_path
        else:
            powerup_name = str(powerup).lower()
            image_path = "../images/" + powerup_name + "/" + powerup_name + "_" + car_path
            
        self.image = pygame.image.load(image_path).convert_alpha()
