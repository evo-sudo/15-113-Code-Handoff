"""
level.py

Forest Temple inspired level layout.

This version is built to resemble the provided screenshot:
- bottom-left Fireboy spawn
- bottom-right Watergirl spawn
- side fans that launch upward
- top ledges
- middle walkway with doors
- lower left/right hazard lanes
- central mound and central island
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
        return [
            # outer frame
            pygame.Rect(0, 0, SCREEN_WIDTH, 20),
            pygame.Rect(0, 0, 20, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),

            # bottom outer spawn blocks
            pygame.Rect(20, 560, 120, 90),
            pygame.Rect(860, 560, 120, 90),

            # bottom left/right hazard lanes
            pygame.Rect(140, 610, 210, 18),
            pygame.Rect(650, 610, 210, 18),

            # lower middle mound
            pygame.Rect(360, 575, 280, 18),
            pygame.Rect(390, 540, 220, 18),
            pygame.Rect(430, 505, 140, 18),

            # middle lower hazard ledges
            pygame.Rect(110, 470, 220, 18),
            pygame.Rect(670, 470, 220, 18),

            # middle main walkway
            pygame.Rect(120, 360, 760, 20),

            # slanted supports approximated as short platforms
            pygame.Rect(155, 345, 40, 15),
            pygame.Rect(805, 345, 40, 15),

            # door alcove floors
            pygame.Rect(220, 325, 75, 18),
            pygame.Rect(705, 325, 75, 18),

            # central island / statue base approximation
            pygame.Rect(445, 300, 110, 18),
            pygame.Rect(470, 265, 60, 18),

            # upper inner puddle ledges
            pygame.Rect(250, 255, 95, 16),
            pygame.Rect(655, 255, 95, 16),

            # upper vertical shafts
            pygame.Rect(205, 145, 18, 180),
            pygame.Rect(777, 145, 18, 180),

            # top left and right walkways
            pygame.Rect(70, 145, 260, 18),
            pygame.Rect(670, 145, 260, 18),

            # side fan shelves
            pygame.Rect(20, 430, 110, 16),
            pygame.Rect(870, 430, 110, 16),
        ]

    def _create_hazards(self):
        return [
            # bottom elemental pools
            {"rect": pygame.Rect(140, 615, 210, 18), "type": "fire"},
            {"rect": pygame.Rect(650, 615, 210, 18), "type": "water"},

            # middle elemental pools
            {"rect": pygame.Rect(120, 475, 200, 16), "type": "water"},
            {"rect": pygame.Rect(680, 475, 200, 16), "type": "fire"},

            # small upper elemental pools
            {"rect": pygame.Rect(255, 260, 85, 12), "type": "fire"},
            {"rect": pygame.Rect(660, 260, 85, 12), "type": "water"},
        ]

    def _create_doors(self):
        return [
            {
                "rect": pygame.Rect(232, 300, 42, 60),
                "type": "fire",
                "label": "F",
            },
            {
                "rect": pygame.Rect(717, 300, 42, 60),
                "type": "water",
                "label": "W",
            },
        ]

    def _create_fans(self):
        return [
            {
                "base_rect": pygame.Rect(35, 416, 70, 14),
                "air_rect": pygame.Rect(40, 150, 60, 266),
            },
            {
                "base_rect": pygame.Rect(895, 416, 70, 14),
                "air_rect": pygame.Rect(900, 150, 60, 266),
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
        for fan in self.fans:
            if player.rect.colliderect(fan["air_rect"]):
                if player.vertical_velocity > -11:
                    player.vertical_velocity = -11
                return

    def draw_hazard(self, surface, hazard):
        rect = hazard["rect"]
        main_color = LAVA_COLOR if hazard["type"] == "fire" else WATER_COLOR
        highlight_color = (255, 200, 120) if hazard["type"] == "fire" else (180, 230, 255)

        pygame.draw.ellipse(surface, main_color, rect)
        inner_rect = pygame.Rect(rect.x + 8, rect.y + 2, rect.width - 16, rect.height - 5)
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

        pygame.draw.rect(surface, (70, 70, 70), base_rect, border_radius=4)
        pygame.draw.rect(surface, (25, 25, 25), base_rect, width=2, border_radius=4)

        for i in range(5):
            x = base_rect.x + 8 + i * 10
            pygame.draw.line(
                surface,
                (200, 200, 200),
                (x, base_rect.y + 2),
                (x, base_rect.y + base_rect.height - 2),
                1,
            )

        for offset in [0, 16, 32]:
            pygame.draw.arc(
                surface,
                (235, 235, 235),
                pygame.Rect(air_rect.x + offset, air_rect.y + 10, 18, 90),
                1.2,
                5.1,
                2,
            )
            pygame.draw.arc(
                surface,
                (235, 235, 235),
                pygame.Rect(air_rect.x + offset, air_rect.y + 105, 18, 90),
                1.2,
                5.1,
                2,
            )
            pygame.draw.arc(
                surface,
                (235, 235, 235),
                pygame.Rect(air_rect.x + offset, air_rect.y + 200, 18, 90),
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