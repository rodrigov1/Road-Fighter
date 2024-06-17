import pygame
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER

class Player(pygame.sprite.Sprite):
    def __init__(self, posX, posY, speed):
        super().__init__()
        self.image = pygame.image.load("images/red_car.png").convert_alpha()
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

    def check_PowerUp(self, powerup):
        # Check if player collided with powerup, if so, return True
        hit = pygame.sprite.spritecollide(self, powerup, True)
        
        return len(hit) > 0
    
    def health(self, health):
        if self.color == "Red":
            match health:
                case 3:
                    self.image = pygame.image.load("images/red_car.png").convert_alpha()
                case 2:
                    self.image = pygame.image.load("images/red_car_1.png").convert_alpha()
                case 1:
                    self.image = pygame.image.load("images/red_car_2.png").convert_alpha()
        else:
            match health:
                case 3:
                    self.image = pygame.image.load("images/dark_blue_car.png").convert_alpha()
                case 2:
                    self.image = pygame.image.load("images/dark_blue_car_1.png").convert_alpha()
                case 1:
                    self.image = pygame.image.load("images/dark_blue_car_2.png").convert_alpha()
                
    def change_car(self, color):
        match color:
            case "Blue":
                self.image = pygame.image.load("images/dark_blue_car.png").convert_alpha()
                self.color = "Blue"
            case "Pink":
                self.image = pygame.image.load("images/pink_car.png").convert_alpha()
            case "Reset":
                self.image = pygame.image.load("images/red_car.png").convert_alpha()
                self.color = "Red"
