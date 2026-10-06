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


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-Defense")

clock = pygame.time.Clock()

game_field = GameField()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()