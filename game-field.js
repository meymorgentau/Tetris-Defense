
const GRID_WIDTH = 10;
const GRID_HEIGHT = 20;

class GameField {
    constructor(width = GRID_WIDTH, height = GRID_HEIGHT) {
        this.width = width;
        this.height = height;

        // Создание пустой матрицы игрового поля
        this.grid = Array.from(
            { length: this.height },
            () => Array(this.width).fill(0)
        );
    }

    // Проверка, занята ли ячейка
    isCellOccupied(row, column) {
        return this.grid[row][column] === 1;
    }

    // Занять ячейку
    occupyCell(row, column) {
        this.grid[row][column] = 1;
    }

    // Освободить ячейку
    clearCell(row, column) {
        this.grid[row][column] = 0;
    }

    // Проверка возможности размещения фигуры
    canPlaceBlock(cells) {
        for (const [column, row] of cells) {
            if (column < 0 || column >= this.width) {
                return false;
            }

            if (row < 0 || row >= this.height) {
                return false;
            }

            if (this.isCellOccupied(row, column)) {
                return false;
            }
        }

        return true;
    }

    // Закрепление фигуры на игровом поле
    lockBlock(cells) {
        for (const [column, row] of cells) {
            if (
                row >= 0 &&
                row < this.height &&
                column >= 0 &&
                column < this.width
            ) {
                this.occupyCell(row, column);
            }
        }
    }

    // Удаление полностью заполненных горизонтальных линий
    clearFullLines() {
        const remainingRows = [];
        const clearedRowIndices = [];

        for (let rowIndex = 0; rowIndex < this.height; rowIndex++) {
            const row = this.grid[rowIndex];

            if (row.every(cell => cell === 1)) {
                clearedRowIndices.push(rowIndex);
            } else {
                remainingRows.push(row);
            }
        }

        const clearedLines = clearedRowIndices.length;

        // Добавление пустых строк сверху поля
        while (remainingRows.length < this.height) {
            remainingRows.unshift(
                Array(this.width).fill(0)
            );
        }

        this.grid = remainingRows;

        return {
            clearedLines,
            clearedRowIndices
        };
    }

    // Проверка возможности появления новой фигуры
    canSpawnBlock(cells) {
        for (const [column, row] of cells) {
            if (row < 0 || row >= this.height) {
                return false;
            }

            if (column < 0 || column >= this.width) {
                return false;
            }

            if (this.isCellOccupied(row, column)) {
                return false;
            }
        }

        return true;
    }
}

// Экспорт класса для использования в других модулях
if (typeof module !== "undefined" && module.exports) {
    module.exports = GameField;
}
