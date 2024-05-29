import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
from unittest.mock import patch,Mock
from screen import Screen, message_display
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
    assert mock_display.update.call_count == 0  # Cambia esta línea



@patch('builtins.quit')
@patch('pygame.font.SysFont')
@patch('pygame.display')
@patch('pygame.event')
def test_game_over(mock_event, mock_display, mock_font, mock_quit):
    screen = Screen()
    # Configura los mocks
    mock_surface = pygame.Surface((800, 600))  # Crea un objeto Surface
    mock_font.return_value.render.return_value = mock_surface  # Hace que render devuelva el objeto Surface
    mock_event.get.side_effect = [[Mock(type=pygame.QUIT)], [Mock(type=pygame.KEYDOWN, key=pygame.K_r)]]
    
    # Llama a la función
    screen.GameOver()
    
    # Verifica que se llamó a las funciones con los argumentos correctos
    assert mock_event.get.call_count == 2
    assert mock_display.update.call_count == 0  # Cambia esta línea
"""