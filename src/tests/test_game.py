import pytest
from pygame import K_ESCAPE, K_RETURN, K_LEFT, K_RIGHT, K_z
from unittest.mock import Mock, patch
from game import Game

# Mock the Game object
@pytest.fixture
def game():
    return Game()

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.sprite.Group')
def test_initPlayerGroup(mock_group, game):
    playerGroup = game.initPlayerGroup()
    assert mock_group.called

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.sprite.Group')
@patch('game.EnemyFactory.create_enemy')
def test_initEnemiesGroup(mock_create_enemy, mock_group, game):
    mock_create_enemy.return_value = Mock()
    enemiesGroup = game.initEnemiesGroup()
    assert mock_group.called
    assert mock_create_enemy.call_count == 5

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('game.Game.initEnemiesGroup')
def test_refreshEnemies(mock_initEnemiesGroup, game):
    mock_initEnemiesGroup.return_value = [Mock(), Mock(), Mock(), Mock(), Mock()]       #Creo el mock de un grupo de enemigos
    enemiesGroup = game.refreshEnemies(300, Mock())
    assert mock_initEnemiesGroup.called


@patch('pygame.sprite.spritecollide')
def test_catchCollisions(mock_spritecollide, game):
    mock_spritecollide.return_value = [Mock()]
    collision = game.catchCollisions(Mock(), Mock())
    assert collision            


@patch('pygame.key.get_pressed')
@patch('pygame.quit')
def test_catchControllerEvents(mock_quit, mock_get_pressed, game):
    mock_get_pressed.return_value = {K_ESCAPE: 1, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 0, K_z: 0}  # verifico que solo se haya presionado una tecla
    game.catchControllerEvents(Mock(), Mock(), Mock())  # llamo a la funcion catchControllerEvents
    mock_get_pressed.assert_called_once()       #verifico que solo se haya llamado una vez a la funcion get_pressed
    mock_quit.assert_called_once()              #dado que se presionó escape verifico que se haya llamado a la funcion quit


@patch('pygame.key.get_pressed')
def test_catchControllerEvents_simple(mock_get_pressed, game):
    game.catchControllerEvents(Mock(), Mock(), Mock())  # llamo a la funcion catchControllerEvents
    mock_get_pressed.assert_called_once()       #verifico que solo se haya llamado una vez a la funcion get_pressed


@patch('pygame.key.get_pressed')
@patch('pygame.quit')
def test_catchControllerEvents_escape(mock_quit, mock_get_pressed, game):
    keys = {K_ESCAPE: 1, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 0, K_z: 0}
    mock_get_pressed.return_value = keys
    game.catchControllerEvents(Mock(), Mock(), Mock())
    mock_quit.assert_called_once()

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.key.get_pressed')
def test_catchControllerEvents_return(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 1, K_LEFT: 0, K_RIGHT: 0, K_z: 0}
    mock_get_pressed.return_value = keys
    playPressed, accelerated = game.catchControllerEvents(Mock(), Mock(), Mock())
    assert playPressed
    assert not accelerated

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.key.get_pressed')
def test_catchControllerEvents_left(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 0, K_LEFT: 1, K_RIGHT: 0, K_z: 0}
    mock_get_pressed.return_value = keys
    mock_playerSprite = Mock()
    game.catchControllerEvents(Mock(), mock_playerSprite, Mock())
    mock_playerSprite.update.assert_called_once_with("left")

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.key.get_pressed')
def test_catchControllerEvents_right(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 1, K_z: 0}
    mock_get_pressed.return_value = keys
    mock_playerSprite = Mock()
    game.catchControllerEvents(Mock(), mock_playerSprite, Mock())
    mock_playerSprite.update.assert_called_once_with("right")

<<<<<<< HEAD
=======

>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.key.get_pressed')
def test_catchControllerEvents_z(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 0, K_z: 1}
    mock_get_pressed.return_value = keys
    playPressed, accelerated = game.catchControllerEvents(Mock(), Mock(), Mock())
    assert not playPressed
    assert accelerated


<<<<<<< HEAD

=======
>>>>>>> 1dc9c718005fbd6362a92137478b4fafa2e710ca
@patch('pygame.display.flip')
@patch('pygame.time.Clock')
#Metodos de la clase game
@patch.object(Game, 'catchEvents')
@patch.object(Game, 'catchControllerEvents')
@patch.object(Game, 'refreshEnemies')
@patch.object(Game, 'catchCollisions')
def test_runGame(mock_catchCollisions, mock_refreshEnemies, mock_catchControllerEvents, mock_catchEvents, mock_Clock, mock_flip, game):
    # Mocks
    mock_screen = Mock()
    mock_clock = Mock()
    mock_playerGroup = Mock()
    mock_enemiesGroup = Mock()
    mock_road = Mock()

    # Configurar los mocks
    mock_playerGroup.sprites.return_value = [Mock()]
    mock_catchControllerEvents.return_value = (True, True)
    mock_refreshEnemies.return_value = mock_enemiesGroup
    mock_catchCollisions.return_value = False

    # Creo esto para que el run game solo se ejecute una sola vez y lance la excepcion, de otra manera se quedaria en un loop infinito
    mock_catchEvents.side_effect = [None, Exception("Stop loop")]       #side_effect simula un comportamiento de la funcion catchEvents
    try:
        game.runGame(mock_screen, mock_clock, mock_playerGroup, mock_enemiesGroup, mock_road)
    except Exception :
        pass

    # Verificar las llamadas a los métodos, todas deberian ser llamadas una vez excepto catchEvents que deberia ser llamada dos veces 
    assert mock_catchEvents.call_count == 2
    mock_catchControllerEvents.assert_called_once_with(mock_road, mock_playerGroup.sprites()[0], mock_enemiesGroup)
    mock_refreshEnemies.assert_called_once()
    mock_catchCollisions.assert_called_once_with(mock_playerGroup.sprites()[0], mock_enemiesGroup)
    mock_flip.assert_called_once()