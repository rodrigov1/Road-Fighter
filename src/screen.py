
import pygame
from player import gameDisplay, display_width, display_height


def message_display(text, shift, color):
    large_text = pygame.font.SysFont(None, 50)
    text_surface = large_text.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (int(display_width / 2), int((display_height / 2) - shift))
    gameDisplay.blit(text_surface, text_rect)
    pygame.display.update()
    
def start_screen(): 
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
        
def game_over():
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