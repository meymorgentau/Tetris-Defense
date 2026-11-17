
class Bullet {
    constructor(x, y) {
        this.width = 6;
        this.height = 12;

        // Начальная позиция пули
        this.x = x - Math.floor(this.width / 2);
        this.y = y;

        // Скорость движения вверх
        this.speed = 8;
    }

    // Перемещение пули вверх
    update() {
        this.y -= this.speed;
    }

    // Проверка выхода пули за экран
    isOutOfScreen(screenHeight = 600) {
        return this.y + this.height < 0;
    }

    // Получение координат прямоугольника пули
    getRect() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }

    // Проверка столкновения с другим прямоугольником
    collidesWith(rect) {
        return (
            this.x < rect.x + rect.width &&
            this.x + this.width > rect.x &&
            this.y < rect.y + rect.height &&
            this.y + this.height > rect.y
        );
    }
}

module.exports = Bullet;
