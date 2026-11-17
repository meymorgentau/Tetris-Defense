
const GameField = require("./game-field.js");
const FallingShape = require("./falling-shape.js");
const Cannon = require("./cannon.js");
const Bullet = require("./bullet.js");

console.log("=== TETRIS DEFENSE: JAVASCRIPT ===");

// 1. Создание игрового поля
const field = new GameField();

console.log("\n1. Игровое поле");
console.log("Размер:", field.width, "x", field.height);

// 2. Создание и движение фигуры
const shape = new FallingShape();

console.log("\n2. Падающая фигура");
console.log("Название:", shape.shapeName);
console.log("Начальная позиция:", shape.x, shape.y);

shape.moveDown(field);

console.log("После движения вниз:", shape.x, shape.y);

// 3. Проверка пушки
const cannon = new Cannon();

console.log("\n3. Пушка");
console.log("Начальная позиция:", cannon.x, cannon.y);

cannon.moveLeft();

console.log("После движения влево:", cannon.x);

// 4. Создание и движение пули
const shotPosition = cannon.getShotPosition();
const bullet = new Bullet(shotPosition[0], shotPosition[1]);

console.log("\n4. Пуля");
console.log("Начальная позиция:", bullet.x, bullet.y);

bullet.update();

console.log("После выстрела:", bullet.x, bullet.y);

// 5. Проверка столкновения пули с фигурой
console.log("\n5. Проверка попадания");

const [cellX, cellY] = shape.getCells()[0];

const testBullet = new Bullet(
    cellX * 30 + 15,
    cellY * 30 + 10
);

const hit = shape.checkBulletCollision(testBullet);

console.log("Попадание:", hit);
console.log("Оставшиеся кубики:", shape.shape.length);

// 6. Закрепление фигуры на поле
field.lockBlock(shape.getCells());

console.log("\n6. Закрепление фигуры");
console.log("Фигура закреплена на поле");

console.log("\n=== ПРОВЕРКА ЗАВЕРШЕНА ===");
