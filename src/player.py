import pygame
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER
from observerp import Subscriber

class Player(Subscriber, pygame.sprite.Sprite):
    def __init__(self, posX, posY, speed):
        super().__init__()
        self.image = pygame.image.load("../images/red_player_3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.posX = posX
        self.posY = posY
        self.speed = speed
        self.rect.center = (posX, posY)
        self.color = "Red"

    def update(self, direction):
        match direction:
            case "right":
                if self.posX < ROAD_RIGHT_BORDER:
                    self.posX += self.speed
            case "left":
                if self.posX > ROAD_LEFT_BORDER:
                    self.posX -= self.speed
            case _:
                pass

        self.rect.center = (self.posX, self.posY)

    def updateHealth(self, health):
        if health > 0:
            image_path = "../images/" + str(self.color).lower() + "_player_" + str(health) + ".png"
            self.image = pygame.image.load(image_path).convert_alpha()

    def updateSub(self, powerup):
        match powerup:
            case "Frozen":
                self.color = "Blue"
            case "Limitless":
                self.color = "Pink"
            case "Reset":
                self.color = "Red"
