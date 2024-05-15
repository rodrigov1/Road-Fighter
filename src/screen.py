import pygame

display_height = 600
display_width = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
bgImage = pygame.image.load("images/road.png")

class Screen():
    def __init__(self):
        gameDisplay.fill((255, 255, 255))
        self.startScreen()
        
    def startScreen(self):
        gameDisplay.fill((255, 255, 255))
        message_display("ROAD FIGHTER", 120, "BLACK")
        message_display("Press P to play", 0, "GREEN")
        message_display("Press Q to quit", -60, "RED")
    
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return
            else:
                continue
    
    def GameOver(self):
        gameDisplay.fill((255, 255, 255))
        message_display("GAME OVER!",45, "RED")
        message_display("Press R to restart or Q to return to menu.",0, "BLACK")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return self.startScreen()
                    elif event.key == pygame.K_r:
                        return
                    
def message_display(text, shift, color):
    large_text = pygame.font.SysFont('freesansbold.ttf', 50)
    text_surface = large_text.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (int(display_width / 2), int((display_height / 2) - shift))
    gameDisplay.blit(text_surface, text_rect)
    pygame.display.update()