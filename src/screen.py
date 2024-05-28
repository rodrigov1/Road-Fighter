import pygame

# ------- Constants for the game -------
ROAD_LEFT_BORDER = 240
ROAD_RIGHT_BORDER = 580
ROAD_WIDTH = ROAD_RIGHT_BORDER - ROAD_LEFT_BORDER
SPRITE_WIDTH = 50
SPRITE_HEIGHT = 50
DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 1200
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


class Screen:
    def startEngine(self):
        # Title window and icon
        pygame.init()
        pygame.display.set_caption("Road Fighter")
        clock = pygame.time.Clock()
        icon = pygame.image.load("../images/car-icon.png")
        pygame.display.set_icon(icon)
        return DISPLAY, clock

    def displayScreen(self, typeScreen):
        if typeScreen == "screenStart":
            menu_image = pygame.image.load("../images/start_menu2.png")
        elif typeScreen == "screenEnd":
            menu_image = pygame.image.load("../images/game_over_menu.png")

        menu_image = pygame.image.load("../images/start_menu2.png")
        # Dibuja la imagen en la pantalla
        DISPLAY.blit(menu_image, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    return
                else:
                    continue
            pygame.display.update()
