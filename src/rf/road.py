import pygame
from rf.observerp import Subscriber
from rf.screen import DISPLAY_HEIGHT
from rf.images import road, limitless_road, frozen_road


class Road(Subscriber):
    def __init__(self, display):
        self.speed = 0
        self.display = display
        self.image = pygame.image.load(road).convert()

    def update(self, speed):
        self.speed += speed

    def draw(self):
        self.newSpeed = self.speed % self.image.get_rect().height
        self.display.blit(self.image, (0, self.newSpeed - self.image.get_rect().height))

        if self.newSpeed < DISPLAY_HEIGHT:
            self.display.blit(self.image, (0, self.newSpeed))

    def updateSub(self, powerup):
        road_path = road
        if powerup == "Reset":
            self.image = pygame.image.load(road).convert()
        else:
            powerup_name = str(powerup).lower()
            road_path = ""
            match powerup_name:
                case "frozen":
                    road_path = frozen_road
                case "limitless":
                    road_path = limitless_road
            self.image = pygame.image.load(road_path).convert()
