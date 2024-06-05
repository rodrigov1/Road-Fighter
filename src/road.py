import pygame
from screen import DISPLAY_HEIGHT

class Road:
    def __init__(self, display):
        self.speed = 0
        self.display = display
        self.image = pygame.image.load("src/images/road.png").convert()

    def update(self, speed):
        self.speed += speed

    def draw(self):
        self.newSpeed = self.speed % self.image.get_rect().height
        self.display.blit(self.image, (0, self.newSpeed - self.image.get_rect().height))
        if self.newSpeed < DISPLAY_HEIGHT:
            self.display.blit(self.image, (0, self.newSpeed))
