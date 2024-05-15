import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from player import Player

display_height = 600
display_width = 800
car_width = 56
car_height = 100

@patch('pygame.sprite.Sprite')
@patch('pygame.image.load')
def test_player_init(mock_image_load, mock_Sprite):
    # Configura los mocks
    mock_image_load.return_value.get_rect.return_value = MagicMock()

    # Crea una instancia de Player
    player = Player()

    # Verifica que se llamó a image.load con los argumentos correctos
    mock_image_load.assert_called_once_with('images/car_player.png')

    # Verifica que la posición inicial del jugador es correcta
    assert player.rect.x == int(display_width * 0.45)
    assert player.rect.y == int(display_height * 0.8)

def test_player_update():
    # Create an instance of Player
    player = Player()

    # Set the initial x_change and y_change
    player.x_change = 10
    player.y_change = 20

    # Call the update method
    player.update()

    # Assert that the rect attributes were updated correctly
    assert player.rect.x == int(display_width * 0.45) + 10
    assert player.rect.y == int(display_height * 0.8) + 20

def test_player_update_boundary_conditions():
    # Create an instance of Player
    player = Player()

    # Test left boundary
    player.x_change = -1000
    player.update()
    assert player.rect.x == 234

    # Test right boundary
    player.x_change = 1000
    player.update()
    assert player.rect.x == 556 - car_width

    # Test top boundary
    player.y_change = -1000
    player.update()
    assert player.rect.y == 0

    # Test bottom boundary
    player.y_change = 1000
    player.update()
    assert player.rect.y == display_height - car_height