"""
settings.py

Stores constants used across the game so they are easy to update in one place.
This makes tuning movement, gravity, colors, and screen size much easier for
whoever continues the project later.
"""

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60
WINDOW_TITLE = "Fireboy and Watergirl - Starter"

# Physics
GRAVITY = 0.6
MOVE_SPEED = 5
JUMP_STRENGTH = 12
MAX_FALL_SPEED = 12

# Player dimensions
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 55

# Colors
BACKGROUND_COLOR = (30, 30, 40)
PLATFORM_COLOR = (140, 120, 90)

FIREBOY_COLOR = (220, 80, 60)
WATERGIRL_COLOR = (70, 150, 255)

LAVA_COLOR = (220, 90, 40)
WATER_COLOR = (60, 140, 230)

TEXT_COLOR = (240, 240, 240)