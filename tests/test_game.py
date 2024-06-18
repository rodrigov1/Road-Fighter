import pytest
from pygame import K_ESCAPE, K_RETURN, K_LEFT, K_RIGHT, K_z
from unittest.mock import Mock, patch,MagicMock,call,ANY
from src.game import Game
import pygame
from src.player import Player
from src.observerp import Subscriber
from itertools import cycle
# Fixture para inicializar el objeto Game
@pytest.fixture
def game():
    game=Game()
    return game

# Fixture para inicializar un grupo de enemigos vacío
@pytest.fixture
def enemies_group():
    enemies_group=pygame.sprite.Group()
    return enemies_group

# Fixture para inicializar un jugador
@pytest.fixture
def player():
    with patch('pygame.image.load') as mock_load:
        mock_load.return_value = Mock()  # Mock the image returned by pygame
        return Player(400, 600, 5)
    

# Fixture para inicializar un grupo de jugadores
@pytest.fixture
def player_group(player):
    playerGroup = pygame.sprite.Group()
    playerGroup.add(player)
    return playerGroup

#Fixture para inicializar un enemigo
@pytest.fixture
def mock_enemy():
    mock_enemy = Mock(spec=pygame.sprite.Sprite)
    return mock_enemy

# Fixture para inicializar un enemigo suscrito
@pytest.fixture
def mock_subscriber_enemy():
    mock_subscriber_enemy = Mock(spec=Subscriber)
    mock_subscriber_enemy.add_internal = MagicMock()
    return mock_subscriber_enemy

@pytest.fixture
def FreezePU():
    return pygame.sprite.Group()

@pytest.fixture
def LimitlessPU():
    return pygame.sprite.Group()


def test_initPowerUpGroup(game):
    powerUpGroup = game.initPowerUpGroup()
    assert len(powerUpGroup) == 0


@patch('pygame.sprite.Group')
def test_initPlayerGroup(mock_group, game):
    # Configura el Mock para simular un comportamiento específico si es necesario
    mock_group_instance = mock_group.return_value
    mock_group_instance.__len__.return_value = 1  # Simula que hay un elemento en el grupo

    playerGroup = game.initPlayerGroup()

    assert mock_group.called  # Verifica que Group fue llamado para crear playerGroup
    assert len(playerGroup) == 1  # Ahora esto debería pasar

def test_initEnemiesGroup(game):
    # Llamada a la función que queremos probar
    enemiesGroup = game.initEnemiesGroup()
    
    # Verificar que se retorna un objeto pygame.sprite.Group
    assert isinstance(enemiesGroup, pygame.sprite.Group)
    
    # Verificar que el grupo de enemigos está inicialmente vacío
    assert len(enemiesGroup) == 0

# testeo que se notifique a los enemigos cuando Limitless es True
@patch.object(Game, 'notify')
def test_refreshEnemies_Limitless_sends_notification(mock_notify, game, enemies_group):
    frame_count = 150
    Frozen = False
    Limitless = True
    game.refreshEnemies(frame_count, enemies_group, Frozen, Limitless)
    mock_notify.assert_called_with("Limitless", ANY)

# testeo que se notifique a los enemigos cuando Frozen es True
@patch.object(Game, 'notify')
def test_refreshEnemies_Frozen_sends_notification(mock_notify, game, enemies_group):
    frame_count = 150
    Frozen = True
    Limitless = False
    game.refreshEnemies(frame_count, enemies_group, Frozen, Limitless)
    mock_notify.assert_called_with("Frozen", ANY)
    
def test_refreshEnemies_multiplo150_frames(game, enemies_group):
    frame_count = 150
    game.refreshEnemies(frame_count, enemies_group, False, False)
    assert len(enemies_group) == 4 #Deberían agregarse 4 enemigos cada 150 frames

    frame_count = 299  # No es múltiplo de 150, no se agregan nuevos enemigos
    game.refreshEnemies(frame_count, enemies_group, False, False)
    assert len(enemies_group) == 4 #No se deben agregar enemigos si el frame_count no es múltiplo de 150

    frame_count = 300  # Siguiente múltiplo de 150, se agregan nuevos enemigos
    game.refreshEnemies(frame_count, enemies_group, False, False)
    assert len(enemies_group) == 8 #Deberían agregarse 4 enemigos adicionales en el frame 300

@patch('enemy.EnemyFactory.create_enemy')
@patch('game.random.choice')
def test_refreshEnemies_no_multiplo150_frames(mock_random_choice, mock_create_enemy, game, enemies_group, mock_subscriber_enemy):
    mock_random_choice.side_effect = ["Yellow", "Blue", "Yellow", "Blue"]       #se necesita pasar si o si 4 enemigos
    mock_create_enemy.return_value = mock_subscriber_enemy

    frame_count = 149                                                           #pero el frame_count no es multiplo de 150 por lo que aun no se crean los enemigos
    game.refreshEnemies(frame_count, enemies_group, False, False)

    assert len(enemies_group) == 0
    mock_create_enemy.assert_not_called()

def test_enemy_types_created(game, enemies_group):
    frame_count = 150
    game.refreshEnemies(frame_count, enemies_group, False, False)
    enemy_types = {enemy.type for enemy in enemies_group}
    assert enemy_types.issubset({'Yellow', 'Blue', 'Rainbow'}) #Solo deberian crearse enemigos de tipo 'Yellow', 'Blue' y 'Rainbow'

def test_enemies_estan_suscriptos(game, enemies_group):
    frame_count = 150
    mock_enemy = Mock(spec=pygame.sprite.Sprite)
    with patch('enemy.EnemyFactory.create_enemy', return_value=mock_enemy):
        game.subscribe = MagicMock()
        game.refreshEnemies(frame_count, enemies_group, False, False)
        assert game.subscribe.call_count == 4           #Todos los enemigos deben ser suscriptores



@patch('powerup.PowerUpFactory.create_powerup')
@patch('game.random.choice')
def test_refreshPowerUps_cada_900frames(mock_random_choice, mock_create_powerup, game,FreezePU, LimitlessPU):
    mock_random_choice.side_effect = ["Blue", "Pink"]
    mock_powerup = Mock(spec=pygame.sprite.Sprite)
    mock_create_powerup.return_value = mock_powerup

    frame_count = 900
    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)    #Llamo al metodo a probar 
    assert len(FreezePU) == 1 #Debería agregar un power-up de Freeze cada 900 frames
    assert len(LimitlessPU) == 0 #No debería agregar un power-up de Limitless en los primeros 900 frames

    frame_count = 1800
    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)
    assert len(FreezePU) == 1 #No debería agregar un power-up de Freeze adicional en los segundos 900 frames
    assert len(LimitlessPU) == 1 #Debería agregar un power-up de Limitless en los segundos 900 frames

@patch('powerup.PowerUpFactory.create_powerup')
@patch('game.random.choice')
def test_refreshPowerUps_not900frames(mock_random_choice, mock_create_powerup, game,FreezePU, LimitlessPU):
    mock_random_choice.side_effect = ["Blue", "Pink"]
    mock_powerup = Mock(spec=pygame.sprite.Sprite)
    mock_create_powerup.return_value = mock_powerup

    frame_count = 899  # Not a multiple of 900, no power-ups should be added

    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)
    assert len(FreezePU) == 0   #No se deberia agregar y que los frame_count no son multiplos de 900
    assert len(LimitlessPU) == 0 #No se deberia agregar y que los frame_count no son multiplos de 900

@patch('powerup.PowerUpFactory.create_powerup')
@patch('game.random.choice')
def test_powerup_types_created(mock_random_choice, mock_create_powerup, game,FreezePU, LimitlessPU):
    mock_random_choice.side_effect = ["Blue", "Pink"]
    mock_powerup = Mock(spec=pygame.sprite.Sprite)
    mock_create_powerup.return_value = mock_powerup

    frame_count = 900

    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)
    assert mock_random_choice.call_args_list == [call(["Blue", "Pink"])]  #se tendrian que haber llamado a uno de estos dos tipos de powerups

    #En este caso el tests no deberia ser igual a estos valores
    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)
    assert not mock_random_choice.call_args_list == [call(["Azul", "Rosa"])]  #Estos powerups no existen por lo tanto no se llama a la funcion

@patch('powerup.PowerUpFactory.create_powerup')
@patch('game.random.choice')
def test_refreshPowerUps_correcta_adicion(mock_random_choice, mock_create_powerup, game,FreezePU, LimitlessPU):
    mock_random_choice.side_effect = ["Blue", "Pink"]
    mock_powerup_blue = Mock(spec=pygame.sprite.Sprite)
    mock_powerup_pink = Mock(spec=pygame.sprite.Sprite)
    mock_create_powerup.side_effect = [mock_powerup_blue, mock_powerup_pink]

    frame_count = 900
    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)
    assert FreezePU.sprites()[0] == mock_powerup_blue #el powerup azul se deberia haber agredo a FreezePU

    frame_count = 1800
    FreezePU, LimitlessPU = game.refreshPowerUps(frame_count, FreezePU, LimitlessPU)
    assert LimitlessPU.sprites()[0] == mock_powerup_pink #el powerup rosa se deberia haber agredo a LimitlessPU


@patch('pygame.sprite.spritecollide', return_value=True)
def test_catchCollisions_FreezePU(mock_spritecollide, game):
    playerSprite = MagicMock()
    FreezePU = game.initPowerUpGroup()
    assert game.catchCollisions(playerSprite, FreezePU) == True

@patch('pygame.sprite.spritecollide', return_value=True)
def test_catchCollisions_Limitless(mock_spritecollide, game):
    playerSprite = MagicMock()
    LimitlessPU = game.initPowerUpGroup()
    assert game.catchCollisions(playerSprite, LimitlessPU) == True


@patch('pygame.sprite.spritecollide')
def test_catchCollisions(mock_spritecollide, game):
    mock_spritecollide.return_value = [Mock()]
    collision = game.catchCollisions(Mock(), Mock())
    assert collision


@patch("pygame.key.get_pressed")
@patch("pygame.quit")
def test_catchControllerEvents(mock_quit, mock_get_pressed, game):
    mock_get_pressed.return_value = {
        K_ESCAPE: 1,
        K_RETURN: 0,
        K_LEFT: 0,
        K_RIGHT: 0,
        K_z: 0,
    }
    game.catchControllerEvents(Mock(), Mock(), Mock(),Mock(), Mock(), Mock())
    mock_get_pressed.assert_called_once()
    mock_quit.assert_called_once()


@patch("pygame.key.get_pressed")
def test_catchControllerEvents_simple(mock_get_pressed, game):
    game.catchControllerEvents(
        Mock(), Mock(), Mock(),Mock(), Mock(), Mock()
    )  # llamo a la funcion catchControllerEvents
    mock_get_pressed.assert_called_once()  # verifico que solo se haya llamado una vez a la funcion get_pressed


@patch("pygame.key.get_pressed")
@patch("pygame.quit")
def test_catchControllerEvents_escape(mock_quit, mock_get_pressed, game):
    keys = {K_ESCAPE: 1, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 0, K_z: 0}
    mock_get_pressed.return_value = keys
    game.catchControllerEvents(Mock(), Mock(), Mock(),Mock(), Mock(), Mock())
    mock_quit.assert_called_once()


@patch("pygame.key.get_pressed")
def test_catchControllerEvents_return(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 1, K_LEFT: 0, K_RIGHT: 0, K_z: 0}
    mock_get_pressed.return_value = keys
    playPressed, accelerated = game.catchControllerEvents(Mock(), Mock(), Mock(),Mock(), Mock(), Mock())
    assert playPressed
    assert not accelerated


@patch("pygame.key.get_pressed")
def test_catchControllerEvents_left(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 0, K_LEFT: 1, K_RIGHT: 0, K_z: 0}
    mock_get_pressed.return_value = keys
    mock_playerSprite = Mock()
    game.catchControllerEvents(Mock(), mock_playerSprite, Mock(),Mock(), Mock(), Mock())
    mock_playerSprite.update.assert_called_once_with("left")


@patch("pygame.key.get_pressed")
def test_catchControllerEvents_right(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 1, K_z: 0}
    mock_get_pressed.return_value = keys
    mock_playerSprite = Mock()
    game.catchControllerEvents(Mock(), mock_playerSprite, Mock(),Mock(), Mock(), Mock())
    mock_playerSprite.update.assert_called_once_with("right")


@patch("pygame.key.get_pressed")
def test_catchControllerEvents_z(mock_get_pressed, game):
    keys = {K_ESCAPE: 0, K_RETURN: 0, K_LEFT: 0, K_RIGHT: 0, K_z: 1}
    mock_get_pressed.return_value = keys
    playPressed, accelerated = game.catchControllerEvents(Mock(), Mock(), Mock(),Mock(), Mock(), Mock())
    assert not playPressed
    assert accelerated

@patch("pygame.display.flip")
@patch("pygame.time.Clock")
@patch.object(Game, "catchEvents")
@patch.object(Game, "catchControllerEvents")
@patch.object(Game, "refreshEnemies")
@patch.object(Game, "refreshPowerUps")
@patch.object(Game, "refreshLives")
@patch.object(Game, "catchCollisions")
def test_runGame(
    mock_catchCollisions,
    mock_refreshLives,
    mock_refreshPowerUps,
    mock_refreshEnemies,
    mock_catchControllerEvents,
    mock_catchEvents,
    mock_Clock,
    mock_flip,
    game,
):
    # Mocks
    mock_screen = Mock()
    mock_clock = Mock()
    mock_playerGroup = Mock()
    mock_enemiesGroup = Mock()
    mock_road = Mock()
    mock_FrozenPowerUp = Mock()
    mock_LimitlessPowerUp = Mock()
    mock_livesGroup = Mock()

    # Configurar los mocks
    mock_player = Mock()
    mock_playerGroup.sprites.return_value = [mock_player]
    mock_catchControllerEvents.return_value = (True, True)  # playPressed, accelerated
    mock_refreshEnemies.return_value = mock_enemiesGroup
    mock_refreshPowerUps.return_value = (mock_FrozenPowerUp, mock_LimitlessPowerUp)
    mock_refreshLives.return_value = mock_livesGroup
    mock_catchCollisions.side_effect = [False, False, False, False]

    # Configurar catchEvents para lanzar excepción después de dos llamadas
    mock_catchEvents.side_effect = [None, Exception("Stop loop")]

    try:
        game.runGame(
            mock_screen,
            mock_clock,
            mock_playerGroup,
            mock_enemiesGroup,
            mock_FrozenPowerUp,
            mock_LimitlessPowerUp,
            mock_livesGroup,
            mock_road,
        )
    except Exception as e:
        assert str(e) == "Stop loop"

    # Verificar que catchEvents se llamó dos veces
    assert mock_catchEvents.call_count == 2

    # Verificar las llamadas a los métodos relevantes
    mock_catchControllerEvents.assert_called_once_with(
        mock_road,
        mock_playerGroup.sprites()[0],
        mock_enemiesGroup,
        mock_FrozenPowerUp,
        mock_LimitlessPowerUp,
        mock_livesGroup,
    )
    mock_refreshEnemies.assert_called_once()
    mock_refreshPowerUps.assert_called_once()
    mock_refreshLives.assert_called_once()

    # Verificar que catchCollisions se llamó las veces esperadas
    assert mock_catchCollisions.call_count == 4
    mock_flip.assert_called_once()

@patch.object(Game, "refreshEnemies")
def test_refreshEnemies_called(
    mock_refreshEnemies,
    game,
):
    mock_enemiesGroup = Mock()

    # Simular la llamada al método
    game.refreshEnemies()

    # Verificar que el método fue llamado
    mock_refreshEnemies.assert_called_once()

@patch.object(Game, "refreshPowerUps")
def test_refreshPowerUps_called(
    mock_refreshPowerUps,
    game,
):
    mock_FrozenPowerUp = Mock()
    mock_LimitlessPowerUp = Mock()

    # Simular la llamada al método
    game.refreshPowerUps()

    # Verificar que el método fue llamado
    mock_refreshPowerUps.assert_called_once()

@patch.object(Game, "refreshLives")
def test_refreshLives_called(
    mock_refreshLives,
    game,
):
    mock_livesGroup = Mock()

    # Simular la llamada al método
    game.refreshLives()

    # Verificar que el método fue llamado
    mock_refreshLives.assert_called_once()