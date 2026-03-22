"""
level.py

Defines the sample level layout used by the game.

This version adds:
- more visible puddles / lava pits
- matching doors
- a cleaner, more temple-like layout
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
        return [
            pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),   # floor
            pygame.Rect(60, 545, 180, 20),
            pygame.Rect(270, 480, 160, 20),
            pygame.Rect(470, 420, 170, 20),
            pygame.Rect(690, 350, 160, 20),
            pygame.Rect(790, 260, 150, 20),
            pygame.Rect(660, 190, 120, 20),
            pygame.Rect(510, 250, 120, 20),
            pygame.Rect(350, 320, 120, 20),
        ]

    def _create_hazards(self):
        """
        Large puddles/lava pits similar to the game style.
        The player only dies if they touch the opposite element.
        """
        floor_y = SCREEN_HEIGHT - 30
        return [
            {"rect": pygame.Rect(110, floor_y, 140, 30), "type": "water"},
            {"rect": pygame.Rect(390, floor_y, 140, 30), "type": "fire"},
            {"rect": pygame.Rect(700, floor_y, 150, 30), "type": "water"},
            {"rect": pygame.Rect(300, 450, 80, 20), "type": "fire"},
            {"rect": pygame.Rect(540, 390, 80, 20), "type": "water"},
        ]

    def _create_doors(self):
        return [
            {
                "rect": pygame.Rect(820, 200, 45, 60),
                "type": "fire",
                "label": "F",
            },
            {
                "rect": pygame.Rect(880, 200, 45, 60),
                "type": "water",
                "label": "W",
            },
        ]

    def check_hazard_collision(self, player):
        for hazard in self.hazards:
            if player.rect.colliderect(hazard["rect"]):
                if hazard["type"] != player.element_type:
                    return True
        return False

    def check_door_collision(self, player):
        for door in self.doors:
            if player.rect.colliderect(door["rect"]):
                if door["type"] == player.element_type:
                    return True
        return False

    def draw_hazard(self, surface, hazard):
        rect = hazard["rect"]
        main_color = LAVA_COLOR if hazard["type"] == "fire" else WATER_COLOR
        highlight_color = (255, 200, 120) if hazard["type"] == "fire" else (180, 230, 255)

        pygame.draw.ellipse(surface, main_color, rect)
        inner_rect = pygame.Rect(rect.x + 8, rect.y + 5, rect.width - 16, rect.height - 10)
        pygame.draw.ellipse(surface, highlight_color, inner_rect)

    def draw_door(self, surface, font, door):
        rect = door["rect"]
        door_color = LAVA_COLOR if door["type"] == "fire" else WATER_COLOR

        pygame.draw.rect(surface, door_color, rect, border_radius=8)
        pygame.draw.rect(surface, (20, 20, 20), rect, width=3, border_radius=8)

        label_surface = font.render(door["label"], True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=rect.center)
        surface.blit(label_surface, label_rect)

    def draw(self, surface, font):
        for platform in self.platforms:
            pygame.draw.rect(surface, PLATFORM_COLOR, platform)

        for hazard in self.hazards:
            self.draw_hazard(surface, hazard)

        for door in self.doors:
            self.draw_door(surface, font, door)