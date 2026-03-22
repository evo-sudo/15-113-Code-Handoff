"""
main.py

Entry point for the Fireboy and Watergirl starter project.

Current scope:
- Two playable characters
- Basic platforming movement
- Gravity and collision
- Simple hazards that reset the player
- Exit doors for both players
- On-screen timer that stops when both players finish
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
    instruction_lines = [
        "Fireboy: A/D to move, W to jump",
        "Watergirl: Left/Right to move, Up to jump",
        "Players do not block each other",
        "Reach the matching doors to finish",
    ]

    for index, line in enumerate(instruction_lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        surface.blit(text_surface, (20, 20 + index * 26))


def format_time(seconds_elapsed):
    minutes = int(seconds_elapsed // 60)
    seconds = int(seconds_elapsed % 60)
    return f"{minutes:02}:{seconds:02}"


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    instruction_font = pygame.font.SysFont(None, 28)
    timer_font = pygame.font.SysFont(None, 36)
    message_font = pygame.font.SysFont(None, 44)

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
    player_finished = {
        "Fireboy": False,
        "Watergirl": False,
    }

    start_time = pygame.time.get_ticks()
    final_time_seconds = None
    game_finished = False

    is_running = True
    while is_running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        pressed_keys = pygame.key.get_pressed()

        if not game_finished:
            for player in players:
                if not player_finished[player.name]:
                    player.update(pressed_keys, level.platforms)

                    if level.check_hazard_collision(player):
                        player.reset_to_spawn()

                    if level.check_door_collision(player):
                        player_finished[player.name] = True

            if all(player_finished.values()):
                game_finished = True
                final_time_seconds = (pygame.time.get_ticks() - start_time) / 1000

        if game_finished:
            timer_value = final_time_seconds
        else:
            timer_value = (pygame.time.get_ticks() - start_time) / 1000

        screen.fill(BACKGROUND_COLOR)
        level.draw(screen, instruction_font)

        for player in players:
            if not player_finished[player.name]:
                player.draw(screen)

        draw_instructions(screen, instruction_font)

        timer_surface = timer_font.render(
            f"Time: {format_time(timer_value)}", True, TEXT_COLOR
        )
        screen.blit(timer_surface, (SCREEN_WIDTH - 180, 20))

        if game_finished:
            complete_surface = message_font.render("Level Complete!", True, TEXT_COLOR)
            complete_rect = complete_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))
            screen.blit(complete_surface, complete_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()