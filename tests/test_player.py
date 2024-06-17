import pytest
from unittest.mock import Mock, patch
from player import Player
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER


# Creo el Mock del escenario
@pytest.fixture
def player():
    with patch("pygame.image.load") as mock_load:
        mock_load.return_value = Mock()  # Mock the image returned by pygame
        return Player(250, 300, 10)


def test_player_initialization(player):
    assert player.posX == 250
    assert player.posY == 300
    assert player.speed == 10
    assert player.rect.center == (250, 300)


def test_player_move_right_within_bounds(player):
    player.update("right")
    assert player.posX == 260
    assert player.rect.center == (260, 300)


# Compruebo si la posicion no cambia cuando estoy en el borde derecho
def test_player_move_right_outside_bounds(player):
    player.posX = ROAD_RIGHT_BORDER
    player.update("right")
    assert player.posX == ROAD_RIGHT_BORDER
    assert player.rect.center == (ROAD_RIGHT_BORDER, 300)


def test_player_move_left_within_bounds(player):
    player.update("left")
    assert player.posX == 240
    assert player.rect.center == (240, 300)


# Compruebo si la posicion no cambia cuando estoy en el borde izquierdo
def test_player_move_left_outside_bounds(player):
    player.posX = ROAD_LEFT_BORDER
    player.update("left")
    assert player.posX == ROAD_LEFT_BORDER
    assert player.rect.center == (ROAD_LEFT_BORDER, 300)


def test_player_update_method_calls(player):
    # Mockeo el metodo update para contar cuantas veces se llama
    player.update = Mock(wraps=player.update)
    player.update("right")
    assert player.update.call_count == 1

    player.update("left")
    assert player.update.call_count == 2


# La posicion no deberia cambiar si la direccion es invalida
def test_player_update_invalid_direction(player):
    original_posX = player.posX
    player.update("invalid_direction")
    assert player.posX == original_posX
