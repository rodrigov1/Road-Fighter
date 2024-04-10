import pygame
import random

pygame.init()

display_height = 600
display_width = 800
car_width = 56
car_height = 100

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Road-Fighter')

carImage = pygame.image.load('images/car.png')
bgImage = pygame.image.load("images/road.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = carImage
        self.rect = self.image.get_rect()
        self.rect.x = (display_width * 0.45)
        self.rect.y = (display_height * 0.8)
        self.x_change = 0
        self.y_change = 0

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        if self.rect.x <= 234.5:
            self.rect.x = 234.5
        elif self.rect.x >= 556 - car_width:
            self.rect.x = 556 - car_width

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= display_height - car_height:
            self.rect.y = display_height - car_height

class OpponentCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = carImage
        self.rect = self.image.get_rect()
        self.rect.x = random.choice((300, 400, 500))
        self.rect.y = -100
        self.speed = random.choice((3, 4, 5, 6, 7, 8))

    def update(self):
        self.rect.y += self.speed

def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    opponents = pygame.sprite.Group()
    for _ in range(4):
        opponent = OpponentCar()
        all_sprites.add(opponent)
        opponents.add(opponent)

    clock = pygame.time.Clock()
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_change = -10
                elif event.key == pygame.K_RIGHT:
                    player.x_change = 10
                elif event.key == pygame.K_UP:
                    player.y_change = -10
                elif event.key == pygame.K_DOWN:
                    player.y_change = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.y_change = 0

        gameDisplay.fill((255, 255, 255))
        gameDisplay.blit(bgImage, (0, 0))

        player.update()
        opponents.update()

        # Generar nuevos obstáculos cuando alguno deje la pantalla
        for opponent in opponents:
            if opponent.rect.y > display_height:
                opponent.rect.x = random.choice((300, 400, 500))
                opponent.rect.y = -100
                opponent.speed = random.choice((3, 4, 5, 6, 7, 8))

        # Verificar colisiones
        if pygame.sprite.spritecollide(player, opponents, False):
            return True

        all_sprites.draw(gameDisplay)
        pygame.display.update()
        clock.tick(60)

    return False

def message_display(text, shift, color):
    large_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surface = large_text.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (display_width / 2, (display_height / 2) - shift)
    gameDisplay.blit(text_surface, text_rect)
    pygame.display.update()

def game_over():
    gameDisplay.fill((255, 255, 255))
    message_display("GAME OVER!",45, "RED")
    message_display("Press R to restart or Q to quit.",0, "BLACK")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    return

def start_screen(): 
    gameDisplay.fill((255, 255, 255))
    message_display("ROAD FIGHTER", 120, "BLACK")
    message_display("Press P to play", 0, "GREEN")
    message_display("Press Q to quit", -60, "RED")
    
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            return
        else:
            continue


# Loop principal del juego
start_screen()

while True:
    if game_loop():
        game_over()
