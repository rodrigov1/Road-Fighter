import pytest
from unittest.mock import Mock, patch
from enemy import Enemy, EnemyFactory
from strategy import StillMovement, ZigZagMovement
from screen import ROAD_LEFT_BORDER, ROAD_RIGHT_BORDER

# Mock the Enemy object
@pytest.fixture
def enemy():
    with patch('pygame.image.load') as mock_load:
        mock_load.return_value = Mock()  # Mock the image returned by pygame
        return Enemy(StillMovement(), "images/yellow_car.png")

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
    assert enemy.rect.x == enemy.posX
    assert enemy.rect.y == enemy.posY - 10
    
#verifica que se cree un enemigo correctamente y que la estrategia de movimiento sea la correcta
def test_enemy_factory():
    yellow_enemy = EnemyFactory.create_enemy("Yellow")
    assert isinstance(yellow_enemy, Enemy)
    assert isinstance(yellow_enemy.movement_strategy, StillMovement)

    blue_enemy = EnemyFactory.create_enemy("Blue")
    assert isinstance(blue_enemy, Enemy)
    assert isinstance(blue_enemy.movement_strategy, ZigZagMovement)

    with pytest.raises(ValueError):
        EnemyFactory.create_enemy("Invalid")
#verifica que se llame a la funcion move de la estrategia de movimiento correctamente
def test_enemy_update_calls_movement_strategy_move(enemy):
    enemy.movement_strategy.move = Mock()
    enemy.update(10)
    enemy.movement_strategy.move.assert_called_once_with(enemy)
#Verifico que la cantidad de veces que se instancia una funcion es correcta
def test_enemy_update_multiples_veces(enemy):
    enemy.movement_strategy.move = Mock()
    
    with pytest.raises(ValueError):
        enemy.update(None)
    
    enemy.update(10)
    enemy.update(10)
    
    assert enemy.movement_strategy.move.call_count == 2

#verifico que la posicion del enemigo este dentro de los limites de la carretera
def test_enemy_position(enemy):
    for _ in range(100):  # Update the enemy multiple times
        enemy.update(10)
    assert ROAD_LEFT_BORDER <= enemy.posX <= ROAD_RIGHT_BORDER
    assert enemy.posY >= 0