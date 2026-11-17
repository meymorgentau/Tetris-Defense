
const Cannon = require("./cannon.js");

const cannon = new Cannon();

console.log("Начальная позиция:", cannon.x, cannon.y);

console.log("Координаты выстрела:", cannon.getShotPosition());

// Проверяем движение влево
cannon.moveLeft();

console.log("После движения влево:", cannon.x);

// Проверяем движение вправо
cannon.moveRight();

console.log("После движения вправо:", cannon.x);

// Проверяем ограничение левой границы
for (let i = 0; i < 100; i++) {
    cannon.moveLeft();
}

console.log("Левая граница:", cannon.x);

// Проверяем ограничение правой границы
for (let i = 0; i < 100; i++) {
    cannon.moveRight();
}

console.log("Правая граница:", cannon.x);
