#def start_screen(): 
#    pygame.event.clear()
#   gameDisplay.blit(start_menu, (0, 0))
#   pygame.display.update()
#   while True:
#       event = pygame.event.wait()
#       if event.type == pygame.QUIT:
#           pygame.quit()
#           sys.exit()
#       elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#           game_loop()
#       else:
#           continue
import pygame
from player import gameDisplay, display_width, display_height

def message_display(text, shift, color):
    large_text = pygame.font.Font('freesansbold.ttf', 50)
    text_surface = large_text.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (int(display_width / 2), int((display_height / 2) - shift))
    gameDisplay.blit(text_surface, text_rect)
    pygame.display.update()
    
def start_screen(): 
    gameDisplay.fill((255, 255, 255))
    message_display("ROAD FIGHTER", 120, "BLACK")
    message_display("Press P to play", 0, "GREEN")
    message_display("Press Q to quit", -60, "RED")
    
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            return
        else:
            continue
        
def game_over():
    gameDisplay.fill((255, 255, 255))
    message_display("GAME OVER!",45, "RED")
    message_display("Press R to restart or Q to quit.",0, "BLACK")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    return        