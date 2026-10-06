import random

import pygame

from constants import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT


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

        self.shape = self.SHAPES[shape_index]
        self.color = self.COLORS[shape_index]

        self.x = GRID_WIDTH // 2 - 1
        self.y = 0

    def move_down(self):
        self.y += 1

    def get_cells(self):
        return [
            (self.x + cell_x, self.y + cell_y)
            for cell_x, cell_y in self.shape
        ]

    def is_at_bottom(self):
        return any(
            cell_y >= GRID_HEIGHT - 1
            for _, cell_y in self.get_cells()
        )

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