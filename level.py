"""
level.py

A more Fireboy-and-Watergirl-inspired sample level.

Features:
- left/right spawn structure
- central platforming route
- elemental pools
- matching doors
- fans that launch players upward
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
    def __init__(self):
        self.platforms = self._create_platforms()
        self.hazards = self._create_hazards()
        self.doors = self._create_doors()
        self.fans = self._create_fans()

    def _create_platforms(self):
        """
        Layout inspired by the screenshot:
        - bottom left/right spawn ledges
        - central lower mound
        - middle walkway
        - upper side structures
        """
        return [
            # bottom spawn ledges
            pygame.Rect(0, 560, 120, 90),
            pygame.Rect(880, 560, 120, 90),

            # lower side ledges above spawn
            pygame.Rect(80, 500, 180, 18),
            pygame.Rect(740, 500, 180, 18),

            # central mound
            pygame.Rect(360, 520, 280, 18),
            pygame.Rect(390, 485, 220, 18),
            pygame.Rect(420, 450, 160, 18),

            # middle long walkway
            pygame.Rect(100, 360, 800, 20),

            # door ledges
            pygame.Rect(220, 325, 90, 18),
            pygame.Rect(690, 325, 90, 18),

            # center upper island
            pygame.Rect(430, 265, 140, 18),

            # upper left structure
            pygame.Rect(90, 145, 200, 18),
            pygame.Rect(210, 145, 18, 180),

            # upper right structure
            pygame.Rect(710, 145, 200, 18),
            pygame.Rect(772, 145, 18, 180),

            # small upper puddle ledges
            pygame.Rect(255, 250, 90, 16),
            pygame.Rect(655, 250, 90, 16),
        ]

    def _create_hazards(self):
        """
        Elemental pools.
        These are meant to sit in open spaces between usable platforms,
        so they feel more like hazards in gaps rather than paint on top.
        """
        return [
            # bottom pools
            {"rect": pygame.Rect(120, 610, 180, 22), "type": "fire"},
            {"rect": pygame.Rect(700, 610, 180, 22), "type": "water"},

            # middle pools
            {"rect": pygame.Rect(150, 430, 160, 20), "type": "water"},
            {"rect": pygame.Rect(690, 430, 160, 20), "type": "fire"},

            # upper small pools
            {"rect": pygame.Rect(260, 266, 80, 14), "type": "fire"},
            {"rect": pygame.Rect(660, 266, 80, 14), "type": "water"},
        ]

    def _create_doors(self):
        return [
            {
                "rect": pygame.Rect(235, 300, 42, 60),
                "type": "fire",
                "label": "F",
            },
            {
                "rect": pygame.Rect(705, 300, 42, 60),
                "type": "water",
                "label": "W",
            },
        ]

    def _create_fans(self):
        """
        Fans are rectangles the player can stand on.
        The air column above them launches players upward.
        """
        return [
            {
                "base_rect": pygame.Rect(10, 485, 70, 15),
                "air_rect": pygame.Rect(15, 250, 60, 235),
            },
            {
                "base_rect": pygame.Rect(920, 485, 70, 15),
                "air_rect": pygame.Rect(925, 250, 60, 235),
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

    def apply_fan_force(self, player):
        """
        If the player is inside a fan's air column, launch them upward.
        """
        for fan in self.fans:
            if player.rect.colliderect(fan["air_rect"]):
                # Strong upward push; only override if falling or moving slowly upward
                if player.vertical_velocity > -8:
                    player.vertical_velocity = -8
                return

    def draw_hazard(self, surface, hazard):
        rect = hazard["rect"]
        main_color = LAVA_COLOR if hazard["type"] == "fire" else WATER_COLOR
        highlight_color = (255, 200, 120) if hazard["type"] == "fire" else (180, 230, 255)

        pygame.draw.ellipse(surface, main_color, rect)

        inner_rect = pygame.Rect(rect.x + 8, rect.y + 3, rect.width - 16, rect.height - 7)
        pygame.draw.ellipse(surface, highlight_color, inner_rect)

        pygame.draw.arc(surface, (40, 30, 20), rect, 0, 3.14, 2)

    def draw_door(self, surface, font, door):
        rect = door["rect"]
        door_color = LAVA_COLOR if door["type"] == "fire" else WATER_COLOR

        pygame.draw.rect(surface, door_color, rect, border_radius=8)
        pygame.draw.rect(surface, (20, 20, 20), rect, width=3, border_radius=8)

        label_surface = font.render(door["label"], True, (255, 255, 255))
        label_rect = label_surface.get_rect(center=rect.center)
        surface.blit(label_surface, label_rect)

    def draw_fan(self, surface, fan):
        base_rect = fan["base_rect"]
        air_rect = fan["air_rect"]

        # fan base
        pygame.draw.rect(surface, (70, 70, 70), base_rect, border_radius=4)
        pygame.draw.rect(surface, (25, 25, 25), base_rect, width=2, border_radius=4)

        # simple fan grill lines
        for i in range(6):
            x = base_rect.x + 8 + i * 10
            pygame.draw.line(
                surface,
                (200, 200, 200),
                (x, base_rect.y + 3),
                (x, base_rect.y + base_rect.height - 3),
                1,
            )

        # air stream
        for offset in [0, 18, 36]:
            pygame.draw.arc(
                surface,
                (235, 235, 235),
                pygame.Rect(air_rect.x + offset, air_rect.y + 20, 18, 80),
                1.2,
                5.1,
                2,
            )
            pygame.draw.arc(
                surface,
                (235, 235, 235),
                pygame.Rect(air_rect.x + offset, air_rect.y + 100, 18, 80),
                1.2,
                5.1,
                2,
            )

    def draw(self, surface, font):
        for platform in self.platforms:
            pygame.draw.rect(surface, PLATFORM_COLOR, platform)

        for hazard in self.hazards:
            self.draw_hazard(surface, hazard)

        for door in self.doors:
            self.draw_door(surface, font, door)

        for fan in self.fans:
            self.draw_fan(surface, fan)