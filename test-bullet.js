
const Bullet = require("./bullet.js");

const bullet = new Bullet(250, 300);

console.log("Начальная позиция:", bullet.x, bullet.y);
console.log("Размер пули:", bullet.width, bullet.height);

// Проверяем движение вверх
bullet.update();

console.log("После движения:", bullet.y);

// Проверяем координаты прямоугольника
console.log("Прямоугольник пули:", bullet.getRect());

// Проверяем столкновение
const target = {
    x: 245,
    y: 280,
    width: 20,
    height: 20
};

console.log("Есть столкновение:", bullet.collidesWith(target));

// Проверяем выход за экран
bullet.y = -20;

console.log("Пуля вышла за экран:", bullet.isOutOfScreen());
