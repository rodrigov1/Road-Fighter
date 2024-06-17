import pygame
import random
from player import Player
from enemy import EnemyFactory
from powerup import PowerUpFactory
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
    
    def initLivesGroup(self):
        livesGroup = pygame.sprite.Group()
        return livesGroup

    def refreshEnemies(self, frame_count, enemiesGroup, Frozen, Limitless):
        if frame_count % 150 == 0:
            for _ in range(4):
                enemy_type = random.choice(["Yellow", "Blue"])
                enemy = EnemyFactory.create_enemy(enemy_type)
                # if Frozen:
                #     enemy.updateSub("Freeze")
                # if Limitless:
                #     enemy.updateSub("Heat")
                enemiesGroup.add(enemy)
                self.subscribe(enemy)

        return enemiesGroup

    def refreshPowerUps(self, frame_count, FreezePU, LimitlessPU):
        if (frame_count % 900 == 0):  # Add new power-up every 900 frames (15 seconds at 60 FPS)
            power = random.choice(["Blue", "Pink"])
            new_powerup = PowerUpFactory.create_powerup(power)
            
            match power:
                case "Blue":
                    FreezePU.add(new_powerup)
                case "Pink":
                    LimitlessPU.add(new_powerup)

        return FreezePU, LimitlessPU
    
    def refreshLives(self, frame_count, livesGroup):
        if (frame_count % 1200 == 0):
            live = EnemyFactory.create_enemy("Rainbow")
            livesGroup.add(live)
        
        return livesGroup

    def catchControllerEvents(self, road, playerSprite, enemiesGroup, FreezePU, LimitlessPU, livesGroup):
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
            FreezePU.update()
            LimitlessPU.update()
            livesGroup.update(5)
            accelerated = True
        else:
            enemiesGroup.update(-5)

        return playPressed, accelerated

    def catchCollisions(self, playerSprite, enemiesGroup, powerUpGroup):
        collision = pygame.sprite.spritecollide(playerSprite, enemiesGroup, False)
        if playerSprite.check_powerUp(powerUpGroup):
            self.notify()  # Notify all subscribers that a power-up has been collected
    def catchCollisions(self, playerSprite, enemiesGroup):
        collision = pygame.sprite.spritecollide(playerSprite, enemiesGroup, True)
        
>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
        return collision != []

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
<<<<<<< HEAD

    def runGame(self, screen, clock, playerGroup, enemiesGroup, powerUpGroup, road):
=======
                
    def catchFrozenPU(self, playerSprite, powerUpGroup, Road, Lives):
        if playerSprite.check_PowerUp(powerUpGroup):
            playerSprite.change_car("Blue")
            playerSprite.health(Lives)
            Road.changeRoad("Freeze")
            self.notify("Freeze")
            Freeze = True
            Frozen_Time = 600
        else:
            Freeze = False
            Frozen_Time = 0
            
        return Freeze, Frozen_Time
    
    def catchLimitlessPU(self, playerSprite, powerUpGroup, Road):
        if playerSprite.check_PowerUp(powerUpGroup):
            playerSprite.change_car("Pink")
            Road.changeRoad("Heat")
            self.notify("Heat")
            Limitless = True
            Invincible_Time = 600
        else:
            Limitless = False
            Invincible_Time = 0
            
        return Limitless, Invincible_Time
    
    def runGame(self, screen, clock, playerGroup, enemiesGroup, FrozenPowerUp, LimitlessPowerUp, livesGroup, road):
        # Player sprite is the only sprite from playerGroup
        playerSprite = playerGroup.sprites()[0]

        # Inicialize variables
        gameRunning = False
        distance = 0
        fuel = 100
        Frozen = False
        Frozen_Time = 0
        Lives = 3
        Limitless = False
        Invincible_Time = 0

        # Frame count
<<<<<<< HEAD
        frame_count = 0
=======
        frame_count = 1
>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca

        while True:
            # Frame inicialization
            screen.fill((0, 0, 0))
            clock.tick(60)

            # Events and controller
            self.catchEvents()
            playPressed, accelerated = self.catchControllerEvents(
<<<<<<< HEAD
                road, playerSprite, enemiesGroup, powerUpGroup
            )
=======
                road, playerSprite,
                enemiesGroup, FrozenPowerUp, LimitlessPowerUp, livesGroup)
>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca

            # Start
            if playPressed and not gameRunning:
                gameRunning = True

            # Refresh
<<<<<<< HEAD
            powerUpGroup = self.refreshPowerUps(frame_count, powerUpGroup)
            enemiesGroup = self.refreshEnemies(frame_count, enemiesGroup)
=======
            FrozenPowerUp, LimitlessPowerUp = self.refreshPowerUps(frame_count, FrozenPowerUp, LimitlessPowerUp)
            enemiesGroup = self.refreshEnemies(frame_count, enemiesGroup, Frozen, Limitless)
            livesGroup = self.refreshLives(frame_count, livesGroup)
>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
            frame_count += 1

            # Gameplay
            if gameRunning and Lives > 0:

                # In Acceleration
                if accelerated:
                    distance += 1
                    fuel -= 0.05

                # Draw objects
                road.draw()
                enemiesGroup.draw(screen)
                playerGroup.draw(screen)
<<<<<<< HEAD
                powerUpGroup.draw(screen)

                # Game collisions
                gameOver = self.catchCollisions(
                    playerSprite, enemiesGroup, powerUpGroup
                )
=======
                FrozenPowerUp.draw(screen)
                LimitlessPowerUp.draw(screen)
                livesGroup.draw(screen)

                # Game collisions
                Crash = self.catchCollisions(playerSprite, enemiesGroup)
                
                Rainbow_Car_Crash = self.catchCollisions(playerSprite, livesGroup)
                
                if Rainbow_Car_Crash:
                    Lives += 1
                    if Lives > 3:
                        Lives = 3
                    playerSprite.health(Lives)
                    
                if Crash and not Limitless:
                    Lives -= 1
                    playerSprite.health(Lives)
                
                # Frozen Time Power Up Effects
                if not Frozen:
                    Frozen, Frozen_Time = self.catchFrozenPU(playerSprite, FrozenPowerUp, road, Lives)
                    
                if Frozen:
                    Frozen_Time -= 1
                    
                    if Frozen_Time <= 0:
                        playerSprite.change_car("Reset")
                        playerSprite.health(Lives)
                        road.changeRoad("Reset")
                        self.notify("Reset")
                        Frozen = False
                        
                if not Limitless:
                    Limitless, Invincible_Time = self.catchLimitlessPU(playerSprite, LimitlessPowerUp, road)
                    
                if Limitless:
                    Invincible_Time -= 1
                    
                    if Invincible_Time <= 0:
                        playerSprite.change_car("Reset")
                        road.changeRoad("Reset")
                        self.notify("Reset")
                        Lives = 3
                        Limitless = False
                    
>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
            else:
                return False

            pygame.display.flip()
