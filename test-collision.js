
const GameField = require("./game-field.js");
const FallingShape = require("./falling-shape.js");
const Bullet = require("./bullet.js");

const field = new GameField();

// Создаём фигуру
const shape = new FallingShape();

console.log("Фигура:", shape.shapeName);
console.log("Начальная позиция:", shape.x, shape.y);

// Проверяем возможность движения вниз
console.log(
    "Можно двигаться вниз:",
    shape.canMoveDown(field)
);

// Перемещаем фигуру вниз
shape.moveDown(field);

console.log("Позиция после движения:", shape.y);

// Проверяем столкновение с дном
shape.y = 17;

console.log(
    "Есть столкновение с дном:",
    shape.hasCollisionBelow(field)
);

// Проверяем попадание пули
shape.y = 5;
shape.x = 2;

const bullet = new Bullet(75, 165);

console.log(
    "Попадание пули:",
    shape.checkBulletCollision(bullet)
);

console.log(
    "Оставшиеся кубики:",
    shape.shape.length
);

console.log(
    "Фигура уничтожена:",
    shape.isDestroyed()
);
