import pygame

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_WIDTH,
    GRID_HEIGHT,
    CELL_SIZE,
    FPS,
    BACKGROUND_COLOR,
    GRID_COLOR
)

from field import GameField
from block import FallingBlock


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-Defense")

clock = pygame.time.Clock()

game_field = GameField()
falling_block = FallingBlock()

running = True

fall_timer = 0
fall_delay = 500

while running:
    delta_time = clock.tick(FPS)
    fall_timer += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if fall_timer >= fall_delay:
        falling_block.move_down()
        fall_timer = 0

        if falling_block.is_at_bottom():
            falling_block = FallingBlock()

    screen.fill(BACKGROUND_COLOR)

    # Рисуем игровое поле
    for row in range(GRID_HEIGHT):
        for column in range(GRID_WIDTH):
            x = column * CELL_SIZE
            y = row * CELL_SIZE

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

    # Рисуем падающий блок
    falling_block.draw(screen)

    pygame.display.flip()

pygame.quit()