
import random

import pygame

from constants import CELL_SIZE, GRID_WIDTH
from shapes_loader import load_shapes


class FallingBlock:
    SHAPES = load_shapes()

    COLORS = {
        "T": (80, 180, 255),
        "Square": (255, 220, 80),
        "I_Horizontal": (180, 100, 255),
        "I_Vertical": (100, 230, 140),
        "Short_I_Horizontal": (255, 120, 100),
        "Short_I_Vertical": (120, 220, 220),
        "L": (220, 140, 255),
        "Reverse_L": (255, 170, 80),
        "Small_L": (140, 200, 120)
    }

    def __init__(self):
        # Выбираем случайную фигуру из конфигурационного файла.
        self.shape_name = random.choice(list(self.SHAPES.keys()))
        self.shape = self.SHAPES[self.shape_name].copy()

        # Назначаем цвет в зависимости от типа фигуры.
        self.color = self.COLORS.get(
            self.shape_name,
            (200, 200, 200)
        )

        # Определяем ширину выбранной фигуры.
        shape_width = max(
            cell_x for cell_x, cell_y in self.shape
        ) + 1

        # Выбираем случайную позицию по ширине игрового поля.
        self.x = random.randint(
            0,
            GRID_WIDTH - shape_width
        )

        self.y = 0

    def get_cells(self, offset_x=0, offset_y=0):
        return [
            (
                self.x + cell_x + offset_x,
                self.y + cell_y + offset_y
            )
            for cell_x, cell_y in self.shape
        ]

    def remove_cell(self, cell):
        if cell in self.shape:
            self.shape.remove(cell)

    def is_destroyed(self):
        return len(self.shape) == 0

    def move_down(self):
        self.y += 1

    def draw(self, screen):
        for cell_x, cell_y in self.get_cells():
            pixel_x = cell_x * CELL_SIZE
            pixel_y = cell_y * CELL_SIZE

            pygame.draw.rect(
                screen,
                self.color,
                (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                (30, 30, 30),
                (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE),
                1
            )
