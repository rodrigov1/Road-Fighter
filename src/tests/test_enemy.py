import sys
import os

import pytest
from unittest.mock import Mock, patch
from enemy import Enemy
"""
@patch('enemy.pygame.sprite.Sprite')
@patch('enemy.pygame.image')
@patch('enemy.random.choice')
def test_enemy_initialization(mock_choice, mock_image, mock_sprite):
    # Mock the random.choice function
    mock_choice.side_effect = [248, 3]

    # Create an instance of Enemy
    enemy = Enemy()

    # Assert that the attributes are initialized correctly
    assert enemy.rect.x == 248
    assert enemy.rect.y == -100
    assert enemy.speed == 3

    # Assert that the necessary methods were called on pygame
    mock_image.load.assert_called_once_with('images/car_enemy.png')

def test_enemy_update():
    # Create an instance of Enemy
    enemy = Enemy()

    # Set the initial speed
    enemy.speed = 5

    # Call the update method
    enemy.update()

    # Assert that the rect.y attribute was updated correctly
    assert enemy.rect.y == -100 + 5
    """