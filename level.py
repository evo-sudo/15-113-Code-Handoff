"""
level.py

Defines the sample level layout used by the game.

This version adds:
- A more reachable platform layout
- Fire and water exit doors
- Hazard checks
- Door checks for win condition
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
    Stores the solid platforms, hazards, and exit doors.
    """

    def __init__(self):
        self.platforms = self._create_platforms()
        self.hazards = self._create_hazards()
        self.doors = self._create_doors()

    def _create_platforms(self):
        """
        Creates a staircase-like layout so both players can actually
        reach the top-right end of the level.
        """
        return [
            pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),   # floor
            pygame.Rect(100, 540, 180, 20),
            pygame.Rect(260, 470, 180, 20),
            pygame.Rect(420, 400, 180, 20),
            pygame.Rect(580, 330, 160, 20),
            pygame.Rect(730, 260, 170, 20),
            pygame.Rect(820, 190, 120, 20),  # final platform near doors
        ]

    def _create_hazards(self):
        return [
            {"rect": pygame.Rect(170, SCREEN_HEIGHT - 30, 120, 30), "type": "water"},
            {"rect": pygame.Rect(500, SCREEN_HEIGHT - 30, 120, 30), "type": "fire"},
        ]

    def _create_doors(self):
        """
        Creates two exit doors at the top-right end of the level.
        Each player must reach their matching door.
        """
        return [
            {
                "rect": pygame.Rect(835, 130, 45, 60),
                "type": "fire",
                "label": "F",
            },
            {
                "rect": pygame.Rect(890, 130, 45, 60),
                "type": "water",
                "label": "W",
            },
        ]

    def check_hazard_collision(self, player):
        """
        Returns True if the player touches the opposite elemental hazard.
        """
        for hazard in self.hazards:
            if player.rect.colliderect(hazard["rect"]):
                if hazard["type"] != player.element_type:
                    return True
        return False

    def check_door_collision(self, player):
        """
        Returns True if the player is touching their matching exit door.
        """
        for door in self.doors:
            if player.rect.colliderect(door["rect"]):
                if door["type"] == player.element_type:
                    return True
        return False

    def draw(self, surface, font):
        for platform in self.platforms:
            pygame.draw.rect(surface, PLATFORM_COLOR, platform)

        for hazard in self.hazards:
            color = LAVA_COLOR if hazard["type"] == "fire" else WATER_COLOR
            pygame.draw.rect(surface, color, hazard["rect"])

        for door in self.doors:
            door_color = LAVA_COLOR if door["type"] == "fire" else WATER_COLOR
            pygame.draw.rect(surface, door_color, door["rect"], border_radius=6)

            label_surface = font.render(door["label"], True, (255, 255, 255))
            label_rect = label_surface.get_rect(center=door["rect"].center)
            surface.blit(label_surface, label_rect)