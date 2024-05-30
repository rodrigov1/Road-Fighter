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
        screen.startScreen()
    
        while True:
            road_fighter.runGame(display, clock, playerGroup, enemiesGroup, road)
            screen.endScreen()
            Start()
        
    Start()