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

    def can_place_block(self, cells):
        for column, row in cells:
            if column < 0 or column >= GRID_WIDTH:
                return False

            if row < 0 or row >= GRID_HEIGHT:
                return False

            if self.is_cell_occupied(row, column):
                return False

        return True

    def lock_block(self, cells):
        for column, row in cells:
            if 0 <= row < GRID_HEIGHT and 0 <= column < GRID_WIDTH:
                self.occupy_cell(row, column)