import pygame
from observerp import Subscriber
from screen import DISPLAY_HEIGHT

class Road(Subscriber):
    def __init__(self, display):
        self.speed = 0
        self.display = display
        self.image = pygame.image.load("../images/road.png").convert()

    def update(self, speed):
        self.speed += speed

    def draw(self):
        self.newSpeed = self.speed % self.image.get_rect().height
        self.display.blit(self.image, (0, self.newSpeed - self.image.get_rect().height))
        
        if self.newSpeed < DISPLAY_HEIGHT:
            self.display.blit(self.image, (0, self.newSpeed))

    def updateSub(self, powerup):
        road_path = "road.png"
        if powerup == "Reset":
            self.image = pygame.image.load("../images/" + road_path).convert()
        else:
            powerup_name = str(powerup).lower()
            self.image = pygame.image.load("../images/" + powerup_name + "/" + powerup_name + "_" + road_path)
            
