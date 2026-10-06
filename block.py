import random

import pygame

from constants import CELL_SIZE, GRID_WIDTH


class FallingBlock:
    SHAPES = [
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (1, 1)
        ],
        [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1)
        ],
        [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0)
        ],
        [
            (0, 0),
            (0, 1),
            (1, 1),
            (2, 1)
        ]
    ]

    COLORS = [
        (80, 180, 255),
        (255, 220, 80),
        (180, 100, 255),
        (100, 230, 140)
    ]

    def __init__(self):
        shape_index = random.randrange(len(self.SHAPES))

        self.shape = self.SHAPES[shape_index].copy()
        self.color = self.COLORS[shape_index]

        self.x = GRID_WIDTH // 2 - 1
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