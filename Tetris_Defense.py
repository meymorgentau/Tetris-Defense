
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
from defense_logger import log_cleared_line


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-Defense")

clock = pygame.time.Clock()


def create_game():
    game_field = GameField()

    active_blocks = [
        {
            "block": FallingBlock(),
            "fall_timer": 0
        }
    ]

    player = Player()

    return game_field, active_blocks, player


def get_active_cells(active_blocks, excluded_block=None):
    cells = set()

    for item in active_blocks:
        block = item["block"]

        if block is excluded_block:
            continue

        cells.update(block.get_cells())

    return cells


def can_spawn_block(new_block, game_field, active_blocks):
    cells = new_block.get_cells()

    if not game_field.can_spawn_block(cells):
        return False

    occupied_cells = get_active_cells(active_blocks)

    return not any(cell in occupied_cells for cell in cells)


def can_move_block_down(block, game_field, active_blocks):
    next_cells = block.get_cells(offset_y=1)

    if not game_field.can_place_block(next_cells):
        return False

    occupied_cells = get_active_cells(
        active_blocks,
        excluded_block=block
    )

    return not any(cell in occupied_cells for cell in next_cells)


game_field, active_blocks, player = create_game()

game_ui = GameUI()

bullets = []

score = 0
cleared_lines = 0

game_over = False
running = True

# Настройки скорости падения
base_fall_delay = 500
minimum_fall_delay = 250

# Настройки появления новых фигур
spawn_timer = 0
base_spawn_delay = 5000
minimum_spawn_delay = 2500


while running:
    delta_time = clock.tick(FPS)

    if not game_over:
        spawn_timer += delta_time

        for item in active_blocks:
            item["fall_timer"] += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Выстрел
            if event.key == pygame.K_SPACE and not game_over:
                bullet_x, bullet_y = player.get_shot_position()

                bullets.append(
                    Bullet(bullet_x, bullet_y)
                )

            # Перезапуск игры
            if event.key == pygame.K_r and game_over:
                game_field, active_blocks, player = create_game()

                bullets.clear()

                score = 0
                cleared_lines = 0

                spawn_timer = 0
                game_over = False

    if not game_over:

        # Управление пушкой
        player.handle_input()

        # Постепенное ускорение падения
        fall_delay = max(
            minimum_fall_delay,
            base_fall_delay - (score // 200) * 25
        )

        # Постепенное увеличение частоты появления фигур
        spawn_delay = max(
            minimum_spawn_delay,
            base_spawn_delay - (score // 300) * 500
        )

        # Создание новых фигур по таймеру
        if spawn_timer >= spawn_delay:
            new_block = FallingBlock()

            if can_spawn_block(
                new_block,
                game_field,
                active_blocks
            ):
                active_blocks.append(
                    {
                        "block": new_block,
                        "fall_timer": 0
                    }
                )

            else:
                # Пробуем другие случайные фигуры и позиции
                spawned = False

                for _ in range(20):
                    new_block = FallingBlock()

                    if can_spawn_block(
                        new_block,
                        game_field,
                        active_blocks
                    ):
                        active_blocks.append(
                            {
                                "block": new_block,
                                "fall_timer": 0
                            }
                        )

                        spawned = True
                        break

                if not spawned:
                    game_over = True
                    bullets.clear()

            spawn_timer = 0

        # Обновление пуль и проверка попаданий
        for bullet in bullets[:]:
            bullet.update()

            if bullet.is_out_of_screen():
                bullets.remove(bullet)
                continue

            bullet_rect = bullet.get_rect()
            hit = False

            for item in active_blocks[:]:
                block = item["block"]

                for cell_x, cell_y in block.get_cells():
                    cell_rect = pygame.Rect(
                        cell_x * CELL_SIZE,
                        cell_y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )

                    if bullet_rect.colliderect(cell_rect):
                        local_cell = (
                            cell_x - block.x,
                            cell_y - block.y
                        )

                        block.remove_cell(local_cell)

                        bullets.remove(bullet)

                        # Очки за уничтожение кубика
                        score += 10

                        # Если уничтожена вся фигура
                        if block.is_destroyed():
                            score += 20
                            active_blocks.remove(item)

                        hit = True
                        break

                if hit:
                    break

        # Независимое падение каждой фигуры
        for item in active_blocks[:]:
            block = item["block"]

            if item["fall_timer"] < fall_delay:
                continue

            if can_move_block_down(
                block,
                game_field,
                active_blocks
            ):
                block.move_down()

            else:
                # Закрепление кубиков на поле
                game_field.lock_block(
                    block.get_cells()
                )

                active_blocks.remove(item)

                # Проверка заполненных линий и получение их индексов
                lines, row_indices = game_field.clear_full_lines()

                # Запись каждой уничтоженной строки в журнал
                for row_index in row_indices:
                    log_cleared_line(row_index)

                cleared_lines += lines
                score += lines * 100

            item["fall_timer"] = 0

        # Проверка возможности продолжения игры
        if not active_blocks:
            test_block = FallingBlock()

            if not can_spawn_block(
                test_block,
                game_field,
                active_blocks
            ):
                game_over = True
                bullets.clear()

    # Отрисовка фона
    screen.fill(BACKGROUND_COLOR)

    # Игровое поле и закреплённые кубики
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

    # Отрисовка всех падающих фигур
    for item in active_blocks:
        item["block"].draw(screen)

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
