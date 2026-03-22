"""
level.py

Defines the sample level layout used by the game.

This file keeps level geometry separate from player code so it is easier to:
- modify the map
- add hazards
- add doors, buttons, gems, or exit zones later

Right now, the level is intentionally small and simple.
"""

import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLATFORM_COLOR,
    LAVA_COLOR,
    WATER_COLOR,
)


class Level:
    """
    Stores the solid platforms and basic hazards.

    Future extension ideas:
    - Separate hazard classes
    - Buttons and doors
    - Collectibles
    - Win zones
    """

    def __init__(self):
        self.platforms = self._create_platforms()
        self.hazards = self._create_hazards()

    def _create_platforms(self):
        """
        Creates the list of solid platforms for collision.

        Using pygame.Rect here keeps the starter version simple and easy to
        debug before introducing more advanced level objects.
        """
        return [
            pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),   # floor
            pygame.Rect(120, 500, 220, 20),
            pygame.Rect(420, 430, 200, 20),
            pygame.Rect(700, 340, 180, 20),
            pygame.Rect(260, 290, 180, 20),
            pygame.Rect(80, 180, 160, 20),
        ]

    def _create_hazards(self):
        """
        Returns hazard data as dictionaries to keep the starter project simple.

        Each hazard has:
        - rect
        - type: 'fire' or 'water'

        Rule idea:
        Fireboy dies in water.
        Watergirl dies in fire.
        """
        return [
            {"rect": pygame.Rect(150, SCREEN_HEIGHT - 30, 120, 30), "type": "water"},
            {"rect": pygame.Rect(500, SCREEN_HEIGHT - 30, 120, 30), "type": "fire"},
        ]

    def check_hazard_collision(self, player):
        """
        Returns True if the player touches a hazard that should defeat them.

        This is intentionally simple so it is easy to extend later.
        """
        for hazard in self.hazards:
            if player.rect.colliderect(hazard["rect"]):
                if hazard["type"] != player.element_type:
                    return True
        return False

    def draw(self, surface):
        for platform in self.platforms:
            pygame.draw.rect(surface, PLATFORM_COLOR, platform)

        for hazard in self.hazards:
            if hazard["type"] == "fire":
                color = LAVA_COLOR
            else:
                color = WATER_COLOR
            pygame.draw.rect(surface, color, hazard["rect"])