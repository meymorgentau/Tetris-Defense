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
from player import Player
from bullet import Bullet


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-Defense")

clock = pygame.time.Clock()

game_field = GameField()
falling_block = FallingBlock()
player = Player()

bullets = []

running = True

fall_timer = 0
fall_delay = 500


while running:
    delta_time = clock.tick(FPS)
    fall_timer += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x, bullet_y = player.get_shot_position()
                bullets.append(Bullet(bullet_x, bullet_y))

    # Управление пушкой
    player.handle_input()

    # Обновление пуль
    for bullet in bullets[:]:
        bullet.update()

        if bullet.is_out_of_screen():
            bullets.remove(bullet)

    # Падение блока
    if fall_timer >= fall_delay:
        next_cells = falling_block.get_cells(offset_y=1)

        if game_field.can_place_block(next_cells):
            falling_block.move_down()
        else:
            game_field.lock_block(falling_block.get_cells())
            game_field.clear_full_lines()

            falling_block = FallingBlock()

        fall_timer = 0

    screen.fill(BACKGROUND_COLOR)

    # Рисуем занятые клетки поля
    for row in range(GRID_HEIGHT):
        for column in range(GRID_WIDTH):
            x = column * CELL_SIZE
            y = row * CELL_SIZE

            if game_field.is_cell_occupied(row, column):
                pygame.draw.rect(
                    screen,
                    (100, 180, 255),
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

            pygame.draw.rect(
                screen,
                GRID_COLOR,
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

    # Рисуем падающий блок
    falling_block.draw(screen)

    # Рисуем пушку
    player.draw(screen)

    # Рисуем пули
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()


pygame.quit()