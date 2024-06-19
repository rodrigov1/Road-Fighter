import pygame
import random
from rf.road import Road
from rf.player import Player
from rf.enemy import EnemyFactory
from rf.powerup import PowerUpFactory
from rf.observerp import Publisher


class Game(Publisher):
    def __init__(self):
        super().__init__()

    def initRoad(self, display):
        road = Road(display)
        self.subscribe(road)
        return road

    def initPowerUpGroup(self):
        powerUpGroup = pygame.sprite.Group()
        return powerUpGroup

    def initPlayerGroup(self):
        player = Player(400, 600, 5)
        playerGroup = pygame.sprite.Group()
        playerGroup.add(player)
        self.subscribe(player)
        return playerGroup

    def initEnemiesGroup(self):
        enemiesGroup = pygame.sprite.Group()
        return enemiesGroup

    def initLivesGroup(self):
        livesGroup = pygame.sprite.Group()
        return livesGroup

    def refreshEnemies(self, frame_count, enemiesGroup, Frozen, Limitless):
        if frame_count % 150 == 0:
            for _ in range(8 if Limitless else 4):
                enemy_type = random.choice(["Yellow", "Blue"])
                enemy = EnemyFactory.create_enemy(enemy_type)
                enemiesGroup.add(enemy)
                self.subscribe(enemy)

                if Frozen:
                    self.notify("Frozen", enemy)
                if Limitless:
                    self.notify("Limitless", enemy)

        return enemiesGroup

    def refreshPowerUps(self, frame_count, FreezePU, LimitlessPU):
        if (
            frame_count % 900 == 0
        ):  # Add new power-up every 900 frames (15 seconds at 60 FPS)
            power = random.choice(["Blue", "Pink"])
            new_powerup = PowerUpFactory.create_powerup(power)

            match power:
                case "Blue":
                    FreezePU.add(new_powerup)
                case "Pink":
                    LimitlessPU.add(new_powerup)

        return FreezePU, LimitlessPU

    def refreshLives(self, frame_count, livesGroup):
        if frame_count % 1200 == 0:
            live = EnemyFactory.create_enemy("Rainbow")
            livesGroup.add(live)

        return livesGroup

    def catchControllerEvents(
        self, road, playerSprite, enemiesGroup, FreezePU, LimitlessPU, livesGroup
    ):
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

    def catchCollisions(self, playerSprite, enemiesGroup):
        collision = pygame.sprite.spritecollide(playerSprite, enemiesGroup, True)
        return collision != []

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def runGame(
        self,
        screen,
        clock,
        playerGroup,
        enemiesGroup,
        freezePowerUp,
        limitlessPowerUp,
        livesGroup,
        road,
    ):
        # Player sprite is the only sprite from playerGroup
        playerSprite = playerGroup.sprites()[0]

        # Inicialize variables
        gameRunning = False
        distance = 0
        fuel = 100
        Frozen = False
        Frozen_Time = 0
        Crash = False
        Lives = 3
        Limitless = False
        Limitless_Time = 0

        # Frame count
        frame_count = 1

        while True:
            # Frame inicialization
            screen.fill((0, 0, 0))
            clock.tick(60)

            # Events and controller
            self.catchEvents()
            playPressed, accelerated = self.catchControllerEvents(
                road,
                playerSprite,
                enemiesGroup,
                freezePowerUp,
                limitlessPowerUp,
                livesGroup,
            )

            # Start
            if playPressed and not gameRunning:
                gameRunning = True

            # Refresh
            freezePowerUp, limitlessPowerUp = self.refreshPowerUps(
                frame_count, freezePowerUp, limitlessPowerUp
            )
            enemiesGroup = self.refreshEnemies(
                frame_count, enemiesGroup, Frozen, Limitless
            )
            livesGroup = self.refreshLives(frame_count, livesGroup)

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
                freezePowerUp.draw(screen)
                limitlessPowerUp.draw(screen)
                livesGroup.draw(screen)

                # Game collisions with enemies/obstacles
                Crash = self.catchCollisions(playerSprite, enemiesGroup)
                RainbowCar_Crash = self.catchCollisions(playerSprite, livesGroup)
                FreezePU_Crash = self.catchCollisions(playerSprite, freezePowerUp)
                LimitlessPU_Crash = self.catchCollisions(playerSprite, limitlessPowerUp)

                # Power Ups Effects
                if LimitlessPU_Crash:
                    Limitless_Time = 600
                    Limitless = True
                    Lives = 3
                    self.notifyAll("Limitless")
                    playerSprite.updateHealth(Lives)

                if Limitless:
                    Limitless_Time -= 1

                    if Limitless_Time <= 0:
                        self.notifyAll("Reset")
                        playerSprite.updateHealth(Lives)
                        Limitless = False

                if RainbowCar_Crash and Lives < 3:
                    Lives += 1
                    playerSprite.updateHealth(Lives)

                if Crash and not Limitless:
                    Lives -= 1
                    playerSprite.updateHealth(Lives)

                # Frozen Time Power Up Effects
                if FreezePU_Crash:
                    Frozen = True
                    Frozen_Time = 600
                    self.notifyAll("Frozen")
                    playerSprite.updateHealth(Lives)

                if Frozen:
                    Frozen_Time -= 1

                    if Frozen_Time <= 0:
                        self.notifyAll("Reset")
                        playerSprite.updateHealth(Lives)
                        Frozen = False

            else:
                return False

            pygame.display.flip()
