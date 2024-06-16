import pygame
import random
from player import Player
from enemy import EnemyFactory
from powerup import PowerUp
from observerp import Publisher

class Game(Publisher):
    def __init__(self):
        super().__init__()

    def initPowerUpGroup(self):
        powerUpGroup = pygame.sprite.Group()
        return powerUpGroup

    def initPlayerGroup(self):
        player = Player(400, 600, 5)
        playerGroup = pygame.sprite.Group()
        playerGroup.add(player)
        
        return playerGroup

    def initEnemiesGroup(self):
        enemiesGroup = pygame.sprite.Group()
        return enemiesGroup

    def refreshEnemies(self, frame_count, enemiesGroup, Frozen):
        if frame_count % 150 == 0:
            for _ in range(4):
                enemy_type = random.choice(["Yellow", "Blue"])
                enemy = EnemyFactory.create_enemy(enemy_type)
                if Frozen:
                    enemy.updateSub("Freeze")
                enemiesGroup.add(enemy)
                self.subscribe(enemy)

        return enemiesGroup

    def refreshPowerUps(self, frame_count, powerUpGroup):
        if (frame_count % 900 == 0):  # Add new power-up every 900 frames (15 seconds at 60 FPS)
            new_powerup = PowerUp()
            powerUpGroup.add(new_powerup)
            
        return powerUpGroup

    def catchControllerEvents(self, road, playerSprite, enemiesGroup, powerUpGroup):
        keys = pygame.key.get_pressed()
        playPressed = False
        accelerated = False

        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        if keys[pygame.K_RETURN]:
            playPressed = True

        if keys[pygame.K_LEFT]:
            playerSprite.update("left")

        if keys[pygame.K_RIGHT]:
            playerSprite.update("right")

        if keys[pygame.K_z]:
            road.update(20)
            enemiesGroup.update(5)
            powerUpGroup.update()
            accelerated = True
        else:
            enemiesGroup.update(-5)

        return playPressed, accelerated

    def catchCollisions(self, playerSprite, enemiesGroup):
        collision = pygame.sprite.spritecollide(playerSprite, enemiesGroup, False)
        
        return collision != []

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
    def catchPowerUp(self, playerSprite, powerUpGroup, Road):
        if playerSprite.check_powerUp(powerUpGroup):
            Road.Freeze(True)
            self.notify("Freeze")
            Freeze = True
            Frozen_Time = 600
        else:
            Freeze = False
            Frozen_Time = 0
            
        return Freeze, Frozen_Time
    
    def runGame(self, screen, clock, playerGroup, enemiesGroup, powerUpGroup, road):
        # Player sprite is the only sprite from playerGroup
        playerSprite = playerGroup.sprites()[0]

        # Inicialize variables
        gameRunning = False
        gameOver = False
        distance = 0
        fuel = 100
        Frozen = False
        Frozen_Time = 0

        # Frame count
        frame_count = 1

        while True:
            # Frame inicialization
            screen.fill((0, 0, 0))
            clock.tick(60)

            # Events and controller
            self.catchEvents()
            playPressed, accelerated = self.catchControllerEvents(
                road, playerSprite, enemiesGroup, powerUpGroup
            )

            # Start
            if playPressed and not gameRunning:
                gameRunning = True

            # Refresh
            powerUpGroup = self.refreshPowerUps(frame_count, powerUpGroup)
            enemiesGroup = self.refreshEnemies(frame_count, enemiesGroup, Frozen)
            frame_count += 1

            # Gameplay
            if gameRunning and not gameOver:

                # In Acceleration
                if accelerated:
                    distance += 1
                    fuel -= 0.05

                # Draw objects
                road.draw()
                enemiesGroup.draw(screen)
                playerGroup.draw(screen)
                powerUpGroup.draw(screen)

                # Game collisions
                gameOver = self.catchCollisions(
                    playerSprite, enemiesGroup)
                
                # Frozen Time Power Up Effects
                if not Frozen:
                    Frozen, Frozen_Time = self.catchPowerUp(playerSprite, powerUpGroup, road)
                    
                if Frozen:
                    Frozen_Time -= 1
                    
                    if Frozen_Time <= 0:
                        road.Freeze(False)
                        self.notify("Reset")
                        Frozen = False
                        
            else:
                return False

            pygame.display.flip()
