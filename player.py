"""
player.py

Defines the Player class used for Fireboy and Watergirl.

This version adds:
- more character-like drawing instead of plain rectangles
- a simple smoke death animation state
- non-blocking players (they still do not collide with each other)
"""

import pygame
from settings import (
    GRAVITY,
    MOVE_SPEED,
    JUMP_STRENGTH,
    MAX_FALL_SPEED,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
)


class Player:
    """
    A controllable character with platformer movement.

    Attributes:
        name: Display/debug name of the character.
        rect: pygame.Rect used for position and collision.
        color: Main character color.
        controls: Dictionary storing movement keys.
        vertical_velocity: Downward/upward speed affected by gravity.
        is_on_ground: Whether the player is standing on something solid.
        element_type: "fire" or "water", useful for hazard logic later.
        spawn_position: Original start location for reset behavior.
        is_dead: Whether the player is currently in death animation.
        death_animation_timer: Counts down the smoke animation.
    """

    def __init__(self, name, start_x, start_y, color, controls, element_type):
        self.name = name
        self.rect = pygame.Rect(start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.controls = controls
        self.element_type = element_type

        self.vertical_velocity = 0
        self.is_on_ground = False
        self.spawn_position = (start_x, start_y)

        self.is_dead = False
        self.death_animation_timer = 0
        self.smoke_center = self.rect.center

    def handle_horizontal_input(self, pressed_keys):
        """
        Reads keyboard input and returns the desired horizontal movement.
        """
        if self.is_dead:
            return 0

        horizontal_change = 0

        if pressed_keys[self.controls["left"]]:
            horizontal_change -= MOVE_SPEED
        if pressed_keys[self.controls["right"]]:
            horizontal_change += MOVE_SPEED

        return horizontal_change

    def try_to_jump(self, pressed_keys):
        """
        Allows jumping only when the player is on the ground.
        """
        if self.is_dead:
            return

        if pressed_keys[self.controls["jump"]] and self.is_on_ground:
            self.vertical_velocity = -JUMP_STRENGTH
            self.is_on_ground = False

    def apply_gravity(self):
        """
        Increases downward speed over time until terminal velocity.
        """
        if self.is_dead:
            return

        self.vertical_velocity += GRAVITY
        if self.vertical_velocity > MAX_FALL_SPEED:
            self.vertical_velocity = MAX_FALL_SPEED

    def move_horizontally(self, horizontal_change, solid_platforms):
        """
        Moves the player left/right and resolves side collisions.
        """
        if self.is_dead:
            return

        self.rect.x += horizontal_change

        for platform in solid_platforms:
            if self.rect.colliderect(platform):
                if horizontal_change > 0:
                    self.rect.right = platform.left
                elif horizontal_change < 0:
                    self.rect.left = platform.right

    def move_vertically(self, solid_platforms):
        """
        Moves the player up/down and resolves floor/ceiling collisions.
        """
        if self.is_dead:
            return

        self.rect.y += self.vertical_velocity
        self.is_on_ground = False

        for platform in solid_platforms:
            if self.rect.colliderect(platform):
                if self.vertical_velocity > 0:
                    self.rect.bottom = platform.top
                    self.vertical_velocity = 0
                    self.is_on_ground = True
                elif self.vertical_velocity < 0:
                    self.rect.top = platform.bottom
                    self.vertical_velocity = 0

    def die(self):
        """
        Starts a short smoke-puff death animation before resetting.
        """
        self.is_dead = True
        self.death_animation_timer = 30
        self.smoke_center = self.rect.center
        self.vertical_velocity = 0
        self.is_on_ground = False

    def update_death_animation(self):
        """
        Updates the smoke animation and resets the player once finished.
        """
        if not self.is_dead:
            return

        self.death_animation_timer -= 1
        if self.death_animation_timer <= 0:
            self.reset_to_spawn()
            self.is_dead = False

    def reset_to_spawn(self):
        """
        Sends the player back to the original spawn point.
        """
        self.rect.topleft = self.spawn_position
        self.vertical_velocity = 0
        self.is_on_ground = False

    def update(self, pressed_keys, solid_platforms):
        """
        Main update function for the character.
        """
        if self.is_dead:
            self.update_death_animation()
            return

        horizontal_change = self.handle_horizontal_input(pressed_keys)
        self.try_to_jump(pressed_keys)
        self.apply_gravity()
        self.move_horizontally(horizontal_change, solid_platforms)
        self.move_vertically(solid_platforms)

    def draw_smoke(self, surface):
        """
        Draws a simple puff-of-smoke style animation.
        """
        progress = 30 - self.death_animation_timer
        radius = 10 + progress

        smoke_color = (220, 220, 220)
        offsets = [(-12, -4), (0, -10), (12, -2), (-6, 10), (8, 8)]

        for dx, dy in offsets:
            pygame.draw.circle(
                surface,
                smoke_color,
                (self.smoke_center[0] + dx, self.smoke_center[1] + dy),
                max(4, radius // 3),
            )

    def draw_character_body(self, surface):
        """
        Draws a simple cartoon body inspired by the two characters.
        This is not sprite art, just a recognizable placeholder style.
        """
        x = self.rect.x
        y = self.rect.y
        w = self.rect.width
        h = self.rect.height

        # head
        head_rect = pygame.Rect(x + 8, y + 2, w - 16, 18)
        pygame.draw.ellipse(surface, self.color, head_rect)

        # eyes
        pygame.draw.circle(surface, (255, 255, 255), (x + 15, y + 10), 3)
        pygame.draw.circle(surface, (255, 255, 255), (x + w - 15, y + 10), 3)
        pygame.draw.circle(surface, (0, 0, 0), (x + 15, y + 10), 1)
        pygame.draw.circle(surface, (0, 0, 0), (x + w - 15, y + 10), 1)

        # body
        body_rect = pygame.Rect(x + 10, y + 18, w - 20, 22)
        pygame.draw.rect(surface, self.color, body_rect, border_radius=6)

        # arms
        pygame.draw.line(surface, self.color, (x + 10, y + 24), (x + 2, y + 34), 4)
        pygame.draw.line(surface, self.color, (x + w - 10, y + 24), (x + w - 2, y + 34), 4)

        # legs
        pygame.draw.line(surface, self.color, (x + 15, y + 40), (x + 10, y + h - 4), 4)
        pygame.draw.line(surface, self.color, (x + w - 15, y + 40), (x + w - 10, y + h - 4), 4)

        # top detail: flame / droplet
        if self.element_type == "fire":
            flame_points = [
                (x + w // 2, y - 8),
                (x + w // 2 - 8, y + 6),
                (x + w // 2, y + 1),
                (x + w // 2 + 8, y + 6),
            ]
            pygame.draw.polygon(surface, (255, 190, 60), flame_points)
        else:
            drop_points = [
                (x + w // 2, y - 6),
                (x + w // 2 - 8, y + 6),
                (x + w // 2, y + 12),
                (x + w // 2 + 8, y + 6),
            ]
            pygame.draw.polygon(surface, (160, 220, 255), drop_points)

    def draw(self, surface):
        if self.is_dead:
            self.draw_smoke(surface)
        else:
            self.draw_character_body(surface)