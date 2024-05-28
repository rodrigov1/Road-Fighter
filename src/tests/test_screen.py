import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from unittest.mock import patch,Mock
from screen import message_display,start_screen,game_over
from player import gameDisplay
import pygame


@patch('pygame.font.SysFont')
@patch('pygame.display')
def test_message_display(mock_display, mock_font):
    # Configura los mocks
    mock_surface = pygame.Surface((100, 100))  # Crea un objeto Surface
    mock_font.return_value.render.return_value = mock_surface  # Hace que render devuelva el objeto Surface

    # Llama a la función
    message_display("Test", 0, "BLACK")

    # Verifica que se llamó a las funciones con los argumentos correctos
    mock_font.assert_called_once_with(None, 50)
    mock_font.return_value.render.assert_called_once_with("Test", True, "BLACK")
    mock_display.update.assert_called_once()

@patch('pygame.event')
@patch('pygame.display')
@patch('pygame.font.SysFont')
@patch('builtins.quit')
def test_start_screen(mock_quit, mock_font, mock_display, mock_event):
    # Configura los mocks
    mock_surface = pygame.Surface((100, 100))  # Crea un objeto Surface
    mock_font.return_value.render.return_value = mock_surface  # Hace que render devuelva el objeto Surface
    mock_event.wait.side_effect = [Mock(type=pygame.QUIT), Mock(type=pygame.KEYDOWN, key=pygame.K_p)]
    
    # Llama a la función
    start_screen()
    
    # Verifica que se llamó a las funciones con los argumentos correctos
    assert mock_event.wait.call_count == 2
    assert mock_display.update.call_count == 3  

