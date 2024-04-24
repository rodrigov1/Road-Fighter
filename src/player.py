import pygame

display_height = 600
display_width = 800
car_width = 56
car_height = 100

bgImage = pygame.image.load("images/road.png")
gameDisplay = pygame.display.set_mode((display_width, display_height))
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/car_player.png')
        self.rect = self.image.get_rect()
        self.rect.x = (int(display_width * 0.45))
        self.rect.y = (int(display_height * 0.8))
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        if self.rect.x <= 234:
            self.rect.x = 234
        elif self.rect.x >= 556 - car_width:
            self.rect.x = 556 - car_width

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= display_height - car_height:
            self.rect.y = display_height - car_height