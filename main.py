"""
main.py

Entry point for the Fireboy and Watergirl starter project.

Current scope:
- Two playable characters
- Basic platforming movement
- Gravity and collision
- Simple hazards that reset the player

This file is meant to be readable first and impressive second.
"""

import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WINDOW_TITLE,
    BACKGROUND_COLOR,
    FIREBOY_COLOR,
    WATERGIRL_COLOR,
    TEXT_COLOR,
)
from player import Player
from level import Level


def draw_instructions(surface, font):
    """
    Draws quick control instructions so the project is easier to test
    without opening the README every time.
    """
    instruction_lines = [
        "Fireboy: A/D to move, W to jump",
        "Watergirl: Left/Right to move, Up to jump",
        "Touching the opposite element resets the player",
    ]

    for index, line in enumerate(instruction_lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        surface.blit(text_surface, (20, 20 + index * 26))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    level = Level()

    fireboy = Player(
        name="Fireboy",
        start_x=80,
        start_y=SCREEN_HEIGHT - 120,
        color=FIREBOY_COLOR,
        controls={
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
        },
        element_type="fire",
    )

    watergirl = Player(
        name="Watergirl",
        start_x=160,
        start_y=SCREEN_HEIGHT - 120,
        color=WATERGIRL_COLOR,
        controls={
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
        },
        element_type="water",
    )

    players = [fireboy, watergirl]

    is_running = True
    while is_running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        pressed_keys = pygame.key.get_pressed()

        for player in players:
            player.update(pressed_keys, level.platforms)

            if level.check_hazard_collision(player):
                player.reset_to_spawn()

        screen.fill(BACKGROUND_COLOR)
        level.draw(screen)

        for player in players:
            player.draw(screen)

        draw_instructions(screen, font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()