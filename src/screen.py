import pygame

display_height = 600
display_width = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
bgImage = pygame.image.load("images/road.png")

class Screen():
    def __init__(self):
        pass
    
    def start_screen(self): 
        # Carga la imagen
        menu_image = pygame.image.load('images/start_menu2.png')
        # Dibuja la imagen en la pantalla
        gameDisplay.blit(menu_image, (0, 0))
        pygame.display.update()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            else:
                continue
        
    def game_over(self):
        # Carga la imagen
        menu_image = pygame.image.load('images/game_over_menu.png')
        # Dibuja la imagen en la pantalla
        gameDisplay.blit(menu_image, (0, 0))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    
                    elif event.key == pygame.K_RETURN:
                        return     