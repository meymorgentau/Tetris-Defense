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
from ui import GameUI


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-Defense")

clock = pygame.time.Clock()


def create_game():
    game_field = GameField()
    falling_block = FallingBlock()
    player = Player()

    return game_field, falling_block, player


game_field, falling_block, player = create_game()

game_ui = GameUI()

bullets = []

score = 0
cleared_lines = 0

game_over = False

running = True

fall_timer = 0
fall_delay = 500


while running:
    delta_time = clock.tick(FPS)

    if not game_over:
        fall_timer += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Выстрел
            if event.key == pygame.K_SPACE and not game_over:
                bullet_x, bullet_y = player.get_shot_position()
                bullets.append(Bullet(bullet_x, bullet_y))

            # Перезапуск игры
            if event.key == pygame.K_r and game_over:
                game_field, falling_block, player = create_game()

                bullets.clear()

                score = 0
                cleared_lines = 0

                fall_timer = 0

                game_over = False

    # Игровая логика работает только до проигрыша
    if not game_over:

        # Управление пушкой
        player.handle_input()

        # Обновление пуль
        for bullet in bullets[:]:
            bullet.update()

            if bullet.is_out_of_screen():
                bullets.remove(bullet)
                continue

            # Проверка столкновения пули с кубиками падающего блока
            bullet_rect = bullet.get_rect()

            for cell in falling_block.get_cells():
                cell_x, cell_y = cell

                cell_rect = pygame.Rect(
                    cell_x * CELL_SIZE,
                    cell_y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                if bullet_rect.colliderect(cell_rect):
                    local_cell = (
                        cell_x - falling_block.x,
                        cell_y - falling_block.y
                    )

                    falling_block.remove_cell(local_cell)

                    bullets.remove(bullet)

                    # Очки за уничтожение кубика
                    score += 10

                    # Если уничтожен весь блок
                    if falling_block.is_destroyed():
                        score += 20
                        falling_block = FallingBlock()

                    break

        # Падение блока
        if fall_timer >= fall_delay:
            next_cells = falling_block.get_cells(offset_y=1)

            if game_field.can_place_block(next_cells):
                falling_block.move_down()

            else:
                # Закрепляем блок на поле
                game_field.lock_block(
                    falling_block.get_cells()
                )

                # Проверяем заполненные линии
                lines = game_field.clear_full_lines()

                cleared_lines += lines

                # Очки за линии
                score += lines * 100

                # Создаём новый блок
                new_block = FallingBlock()

                # Проверяем возможность его появления
                if game_field.can_spawn_block(
                    new_block.get_cells()
                ):
                    falling_block = new_block
                else:
                    game_over = True

                    bullets.clear()

            fall_timer = 0

    screen.fill(BACKGROUND_COLOR)

    # Игровое поле
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

    # Падающий блок
    if not game_over:
        falling_block.draw(screen)

    # Пушка
    player.draw(screen)

    # Пули
    for bullet in bullets:
        bullet.draw(screen)

    # Интерфейс
    game_ui.draw_game_info(
        screen,
        score,
        cleared_lines
    )

    # Экран проигрыша
    if game_over:
        game_ui.draw_game_over(
            screen,
            score,
            cleared_lines
        )

    pygame.display.flip()


pygame.quit()