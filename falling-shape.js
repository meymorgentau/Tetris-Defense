
const loadShapes = require("./shapes-loader.js");

const GRID_WIDTH = 10;
const CELL_SIZE = 30;

class FallingShape {
    static SHAPES = loadShapes();

    static COLORS = {
        "T": [80, 180, 255],
        "Square": [255, 220, 80],
        "I_Horizontal": [180, 100, 255],
        "I_Vertical": [100, 230, 140],
        "Short_I_Horizontal": [255, 120, 100],
        "Short_I_Vertical": [120, 220, 220],
        "L": [220, 140, 255],
        "Reverse_L": [255, 170, 80],
        "Small_L": [140, 200, 120],
        "O": [255, 150, 200]
    };

    static firstShapeName = "O";
    static firstShapeUsed = false;

    constructor() {
        if (!FallingShape.firstShapeUsed) {
            this.shapeName = FallingShape.firstShapeName;
            FallingShape.firstShapeUsed = true;
        } else {
            const names = Object.keys(FallingShape.SHAPES);

            this.shapeName = names[
                Math.floor(Math.random() * names.length)
            ];
        }

        this.shape = FallingShape.SHAPES[this.shapeName].map(
            cell => [...cell]
        );

        this.color = FallingShape.COLORS[this.shapeName] || [200, 200, 200];

        const shapeWidth = Math.max(
            ...this.shape.map(cell => cell[0])
        ) + 1;

        this.x = Math.floor(
            Math.random() * (GRID_WIDTH - shapeWidth + 1)
        );

        this.y = 0;
    }

    // Получение координат кубиков
    getCells(offsetX = 0, offsetY = 0) {
        return this.shape.map(([cellX, cellY]) => [
            this.x + cellX + offsetX,
            this.y + cellY + offsetY
        ]);
    }

    // Проверка столкновения с дном или другими блоками
    hasCollisionBelow(field) {
        return !field.canPlaceBlock(this.getCells(0, 1));
    }

    // Проверка возможности движения вниз
    canMoveDown(field) {
        return field.canPlaceBlock(this.getCells(0, 1));
    }

    // Перемещение вниз с проверкой столкновения
    moveDown(field = null) {
        if (field !== null && !this.canMoveDown(field)) {
            return false;
        }

        this.y += 1;
        return true;
    }

    // Удаление отдельного кубика
    removeCell(cell) {
        const index = this.shape.findIndex(
            ([x, y]) => x === cell[0] && y === cell[1]
        );

        if (index !== -1) {
            this.shape.splice(index, 1);
        }
    }

    // Проверка столкновения пули с кубиками фигуры
    checkBulletCollision(bullet, cellSize = CELL_SIZE) {
        const bulletRect = bullet.getRect();

        for (let i = 0; i < this.shape.length; i++) {
            const [cellX, cellY] = this.shape[i];

            const cellRect = {
                x: (this.x + cellX) * cellSize,
                y: (this.y + cellY) * cellSize,
                width: cellSize,
                height: cellSize
            };

            if (bullet.collidesWith(cellRect)) {
                this.shape.splice(i, 1);
                return true;
            }
        }

        return false;
    }

    // Проверка полного уничтожения фигуры
    isDestroyed() {
        return this.shape.length === 0;
    }
}

module.exports = FallingShape;
