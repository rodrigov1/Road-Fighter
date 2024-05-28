from road import Road
from screen import Screen
from game import Game

if __name__ == "__main__":
    screen = Screen()
    display, clock = screen.startEngine()
    road = Road(display)
    road_fighter = Game()
    playerGroup = road_fighter.initPlayerGroup()
    enemiesGroup = road_fighter.initEnemiesGroup()
    screen.displayScreen("screenStart")
    road_fighter.runGame(display, clock, playerGroup, enemiesGroup, road)
    screen.displayScreen("screenEnd")
