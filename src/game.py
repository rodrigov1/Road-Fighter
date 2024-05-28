import pygame
import random
from player import Player
from enemy import Enemy
from screen import Screen, display_height, gameDisplay, bgImage

pygame.init()
pygame.display.set_caption('Road-Fighter')

class Game():
    def __init__(self):
        self.gameExit = False
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.opponents = pygame.sprite.Group()
    
    def reset(self):
        self.opponents.empty()  # Remove all opponents
        self.all_sprites.empty()  # Remove all sprites

    def game_loop(self):
        player = Player()
        self.all_sprites.add(player)
        
        for _ in range(5):
            opponent = Enemy()
            self.all_sprites.add(opponent)
            self.opponents.add(opponent)

        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
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

            player.update()
            gameDisplay.blit(bgImage, (0, 0))
            self.opponents.update()

            # Generar nuevos obstáculos cuando alguno deje la pantalla
            for opponent in self.opponents:
                if opponent.rect.y > display_height:
                    opponent.rect.x = random.choice((248,332,420,500))
                    opponent.rect.y = -100
                    opponent.speed = random.choice((3, 4, 5, 6, 7, 8))

            # Verificar colisiones
            if pygame.sprite.spritecollide(player, self.opponents, False):
                return True

            self.all_sprites.draw(gameDisplay)
            pygame.display.update()
            self.clock.tick(60)

        return False

# Loop principal del juego
start = Screen()
start.startScreen()
RoadFighter = Game()

while True:
    if RoadFighter.game_loop():  # If the game is over
        start.GameOver()  # Pass the player to the game_over function
        RoadFighter.reset()  # Reset the game