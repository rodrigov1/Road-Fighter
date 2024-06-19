import pytest
from unittest.mock import Mock, patch
from rf.enemy import Enemy, EnemyFactory
from rf.strategy import StillMovement, ZigZagMovement
from rf.screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER
from rf.images import *


@pytest.fixture
def enemy():
    with patch("pygame.image.load") as mock_load:
        mock_load.return_value = Mock()  # Mock the image returned by pygame
        return Enemy(StillMovement(), yellow_car, "Yellow")


def test_enemy_initialization(enemy):
    assert enemy.posX >= ROAD_LEFT_BORDER
    assert enemy.posX <= ROAD_RIGHT_BORDER
    assert enemy.posY <= 0
    assert enemy.speed == 0
    assert enemy.rect.x == enemy.posX
    assert enemy.rect.y == enemy.posY


def test_enemy_update(enemy):
    original_posX = enemy.posX
    original_posY = enemy.posY
    enemy.update(10)
    assert enemy.speed == 10
    assert enemy.posX != original_posX or enemy.posY != original_posY


def test_enemy_factory():
    with patch("rf.enemy.StillMovement", autospec=True) as mock_still_movement, patch(
        "rf.enemy.ZigZagMovement", autospec=True
    ) as mock_zigzag_movement:

        # Yellow enemy
        yellow_enemy = EnemyFactory.create_enemy("Yellow")
        assert isinstance(yellow_enemy, Enemy)
        assert yellow_enemy.movement_strategy == mock_still_movement.return_value

        # Blue enemy
        blue_enemy = EnemyFactory.create_enemy("Blue")
        assert isinstance(blue_enemy, Enemy)
        assert blue_enemy.movement_strategy == mock_zigzag_movement.return_value

        # Invalid enemy type
        with pytest.raises(ValueError):
            EnemyFactory.create_enemy("InvalidType")


# verifica que se llame a la funcion move de la estrategia de movimiento correctamente
def test_enemy_update_calls_movement_strategy_move(enemy):
    enemy.movement_strategy.move = Mock()
    enemy.update(10)
    enemy.movement_strategy.move.assert_called_once_with(enemy)


# Verifico que la cantidad de veces que se instancia una funcion es correcta
def test_enemy_update_multiples_veces(enemy):
    enemy.movement_strategy.move = Mock()

    with pytest.raises(ValueError):
        enemy.update(None)

    enemy.update(10)
    enemy.update(10)

    assert enemy.movement_strategy.move.call_count == 2


# Verifico que la posicion del enemigo este dentro de los limites de la carretera
def test_enemy_position(enemy):
    for _ in range(100):  # Update the enemy multiple times
        enemy.update(10)
    assert ROAD_LEFT_BORDER <= enemy.posX <= ROAD_RIGHT_BORDER
    assert enemy.posY >= 0


def test_enemy_updateSub_Frozen(enemy):
    with patch("rf.enemy.StillMovement", autospec=True) as mock_still_movement:
        enemy.updateSub("Frozen")
        assert isinstance(
            enemy.movement_strategy, type(mock_still_movement.return_value)
        )


def test_enemy_updateSub_Limitless(enemy):
    with patch("rf.enemy.ZigZagMovement", autospec=True) as mock_zigzag_movement:
        enemy.updateSub("Limitless")
        assert isinstance(
            enemy.movement_strategy, type(mock_zigzag_movement.return_value)
        )


def test_enemy_updateSub_Reset_Blue(enemy):
    with patch("rf.enemy.ZigZagMovement", autospec=True) as mock_zigzag_movement:
        # Create a blue enemy specifically for this test
        blue_enemy = EnemyFactory.create_enemy("Blue")
        blue_enemy.updateSub("Reset")
        assert isinstance(
            blue_enemy.movement_strategy, type(mock_zigzag_movement.return_value)
        )


def test_enemy_updateSub_Reset_Yellow(enemy):
    with patch("rf.enemy.StillMovement", autospec=True) as mock_still_movement:
        # Create a yellow enemy specifically for this test
        yellow_enemy = EnemyFactory.create_enemy("Yellow")
        yellow_enemy.updateSub("Reset")
        assert isinstance(
            yellow_enemy.movement_strategy, type(mock_still_movement.return_value)
        )


def test_enemy_updateSub_Reset_Rainbow(enemy):
    with patch("rf.enemy.StillMovement", autospec=True) as mock_still_movement:
        # Create a rainbow enemy specifically for this test
        rainbow_enemy = EnemyFactory.create_enemy("Rainbow")
        rainbow_enemy.updateSub("Reset")
        assert isinstance(
            rainbow_enemy.movement_strategy, type(mock_still_movement.return_value)
        )


def test_enemy_initialization_with_type():
    yellow_enemy = EnemyFactory.create_enemy("Yellow")
    assert yellow_enemy.type == "Yellow"
    blue_enemy = EnemyFactory.create_enemy("Blue")
    assert blue_enemy.type == "Blue"
    rainbow_enemy = EnemyFactory.create_enemy("Rainbow")
    assert rainbow_enemy.type == "Rainbow"

    with pytest.raises(ValueError):
        EnemyFactory.create_enemy("InvalidType")
