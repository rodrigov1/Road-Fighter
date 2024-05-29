import pygame
from player import Player
from enemy import EnemyFactory


class Game:
    def initPlayerGroup(self):
        # Posicion centrada
        player = Player(400, 600, 5)
        playerGroup = pygame.sprite.Group()
        playerGroup.add(player)
        return playerGroup

    def initEnemiesGroup(self):
        enemiesGroup = pygame.sprite.Group()
        for _ in range(5):
            enemy_type = "Yellow"
            enemy = EnemyFactory.create_enemy(enemy_type)
            enemiesGroup.add(enemy)
        return enemiesGroup
    
    def refreshEnemies(self, frame_count, enemiesGroup):
        if frame_count % 300 == 0:
            new_enemies = self.initEnemiesGroup()
            for enemy in new_enemies:
                enemiesGroup.add(enemy)
        return enemiesGroup

    def catchControllerEvents(self, road, playerSprite, enemiesGroup):
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
            accelerated = True
        else:
            enemiesGroup.update(-5)

        return playPressed, accelerated

    def catchCollisions(self, playerSprite, enemiesGroup):
        collision = pygame.sprite.spritecollide(playerSprite, enemiesGroup, False)
        return collision

    def catchEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def runGame(self, screen, clock, playerGroup, enemiesGroup, road):
        # Player sprite is the only sprite from playerGroup
        playerSprite = playerGroup.sprites()[0]

        # Inicialize variables
        gameRunning = False
        gameOver = False
        distance = 0
        fuel = 100

        #Frame count
        frame_count=0

        while True:
            # Frame inicialization
            screen.fill((0, 0, 0))
            clock.tick(60)

            # Events and controller
            self.catchEvents()
            playPressed, accelerated = self.catchControllerEvents(
                road, playerSprite, enemiesGroup
            )

            # Start
            if playPressed and not gameRunning:
                gameRunning = True

            # Refresh
            enemiesGroup=self.refreshEnemies(frame_count, enemiesGroup)
            frame_count+=1

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

                # Game collisions
                gameOver = self.catchCollisions(playerSprite, enemiesGroup)


            pygame.display.flip()
