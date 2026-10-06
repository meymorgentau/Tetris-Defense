from constants import GRID_WIDTH, GRID_HEIGHT


class GameField:
    def __init__(self):
        self.grid = [
            [0 for _ in range(GRID_WIDTH)]
            for _ in range(GRID_HEIGHT)
        ]

    def is_cell_occupied(self, row, column):
        return self.grid[row][column] == 1

    def occupy_cell(self, row, column):
        self.grid[row][column] = 1

    def clear_cell(self, row, column):
        self.grid[row][column] = 0
