from road import Road
from screen import Screen
from game import Game

if __name__ == "__main__":

    def Start():
        screen = Screen()
        display, clock = screen.startEngine()
        road = Road(display)
        road_fighter = Game()
        playerGroup = road_fighter.initPlayerGroup()
        enemiesGroup = road_fighter.initEnemiesGroup()
        FrozenPowerUp = road_fighter.initPowerUpGroup()
        LimitlessPowerUp = road_fighter.initPowerUpGroup()
        livesGroup = road_fighter.initLivesGroup()
        screen.startScreen()
        

        while True:
            road_fighter.runGame(display, clock, playerGroup, 
                enemiesGroup, FrozenPowerUp,
                LimitlessPowerUp, livesGroup, road)
            screen.endScreen()
            Start()

    Start()