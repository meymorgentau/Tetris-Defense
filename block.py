import random

import pygame

from constants import CELL_SIZE, GRID_WIDTH


class FallingBlock:
    SHAPES = [
        # T
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (1, 1)
        ],

        # Square
        [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1)
        ],

        # I horizontal
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0)
        ],

        # I vertical
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3)
        ],

        # I short horizontal
        [
            (0, 0),
            (1, 0)
        ],

        # I short vertical
        [
            (0, 0),
            (0, 1)
        ],

        # L
        [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2)
        ],

        # Reverse L
        [
            (1, 0),
            (1, 1),
            (1, 2),
            (0, 2)
        ],

        # Small L
        [
            (0, 0),
            (0, 1),
            (1, 1)
        ]
    ]

    COLORS = [
        (80, 180, 255),
        (255, 220, 80),
        (180, 100, 255),
        (100, 230, 140),
        (255, 120, 100),
        (120, 220, 220),
        (220, 140, 255),
        (255, 170, 80),
        (140, 200, 120)
    ]

    def __init__(self):
        shape_index = random.randrange(len(self.SHAPES))

        self.shape = self.SHAPES[shape_index].copy()
        self.color = self.COLORS[shape_index]

        # Определяем ширину выбранной фигуры
        shape_width = max(
            cell_x for cell_x, cell_y in self.shape
        ) + 1

        # Случайная позиция по всей ширине игрового поля
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