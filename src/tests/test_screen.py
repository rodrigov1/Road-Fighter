import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from unittest.mock import patch,Mock
from screen import Screen, gameDisplay
import pygame

@patch('pygame.event')
@patch('pygame.display')
@patch('pygame.font.SysFont')
def test_start_screen(mock_font, mock_display, mock_event):
    # Configura los mocks
    mock_surface = pygame.Surface((100, 100))  # Crea un objeto Surface
    mock_font.return_value.render.return_value = mock_surface  # Hace que render devuelva el objeto Surface
    mock_event.wait.side_effect = [Mock(type=pygame.QUIT), Mock(type=pygame.KEYDOWN, key=pygame.K_p)]
    
    # Llama a la función
    screen = Screen()
    screen.start_screen()
    
    # Verifica que se llamó a las funciones con los argumentos correctos
    assert mock_event.wait.call_count == 2
    assert mock_display.update.call_count == 3  

