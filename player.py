"""
player.py

Defines the Player class used for Fireboy and Watergirl.

Design goal:
- Keep movement and collision logic easy to read.
- Use descriptive variable names instead of short names like vx/vy.
- Separate horizontal and vertical collision steps because that is easier for
  another student to debug and extend.
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
        color: RGB color for drawing the character.
        controls: Dictionary storing movement keys.
        vertical_velocity: Downward/upward speed affected by gravity.
        is_on_ground: Whether the player is standing on something solid.
        element_type: "fire" or "water", useful for hazard logic later.
        spawn_position: Original start location for reset behavior.
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

    def handle_horizontal_input(self, pressed_keys):
        """
        Reads keyboard input and returns the desired horizontal movement.
        We return a number instead of moving directly so the main update flow
        stays predictable and easier to modify later.
        """
        horizontal_change = 0

        if pressed_keys[self.controls["left"]]:
            horizontal_change -= MOVE_SPEED
        if pressed_keys[self.controls["right"]]:
            horizontal_change += MOVE_SPEED

        return horizontal_change

    def try_to_jump(self, pressed_keys):
        """
        Allows jumping only when the player is on the ground.

        Why this matters:
        Restricting jumps here keeps the jump rule in one place, which is easier
        to extend later if someone wants double-jumps, wall-jumps, etc.
        """
        if pressed_keys[self.controls["jump"]] and self.is_on_ground:
            self.vertical_velocity = -JUMP_STRENGTH
            self.is_on_ground = False

    def apply_gravity(self):
        """
        Increases downward speed over time until terminal velocity.
        """
        self.vertical_velocity += GRAVITY
        if self.vertical_velocity > MAX_FALL_SPEED:
            self.vertical_velocity = MAX_FALL_SPEED

    def move_horizontally(self, horizontal_change, solid_platforms):
        """
        Moves the player left/right and resolves side collisions.
        """
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
        self.rect.y += self.vertical_velocity
        self.is_on_ground = False

        for platform in solid_platforms:
            if self.rect.colliderect(platform):
                if self.vertical_velocity > 0:
                    # Landing on top of a platform
                    self.rect.bottom = platform.top
                    self.vertical_velocity = 0
                    self.is_on_ground = True
                elif self.vertical_velocity < 0:
                    # Hitting the underside of a platform
                    self.rect.top = platform.bottom
                    self.vertical_velocity = 0

    def reset_to_spawn(self):
        """
        Sends the player back to the original spawn point.
        This is useful for hazards and keeps failure handling simple.
        """
        self.rect.topleft = self.spawn_position
        self.vertical_velocity = 0
        self.is_on_ground = False

    def update(self, pressed_keys, solid_platforms):
        """
        Main update function for the character.

        Order matters:
        1. Read movement input
        2. Attempt jump
        3. Apply gravity
        4. Resolve horizontal movement
        5. Resolve vertical movement

        This order makes platform collisions feel stable and is easier to reason
        about than mixing every action together.
        """
        horizontal_change = self.handle_horizontal_input(pressed_keys)
        self.try_to_jump(pressed_keys)
        self.apply_gravity()
        self.move_horizontally(horizontal_change, solid_platforms)
        self.move_vertically(solid_platforms)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)