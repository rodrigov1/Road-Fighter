import pygame
from rf.screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER
from rf.observerp import Subscriber
from rf.images import red_player_3, red_player_2, red_player_1


class Player(Subscriber, pygame.sprite.Sprite):
    def __init__(self, posX, posY, speed):
        super().__init__()
        self.image = pygame.image.load(red_player_3).convert_alpha()
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
            image_path = red_player_1
            match health:
                case 1:
                    image_path = red_player_1
                case 2:
                    image_path = red_player_2
                case 3:
                    image_path = red_player_3
            self.image = pygame.image.load(image_path).convert_alpha()

    def updateSub(self, powerup):
        match powerup:
            case "Frozen":
                self.color = "Blue"
            case "Limitless":
                self.color = "Pink"
            case "Reset":
                self.color = "Red"
