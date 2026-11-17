
const GameField = require("./game-field.js");
const FallingShape = require("./falling-shape.js");

const field = new GameField();
const shape = new FallingShape();

// Создаём препятствие в нижней строке
const obstacle = [];

for (let column = 0; column < 10; column++) {
    obstacle.push([column, 19]);
}

field.lockBlock(obstacle);

console.log("Создано препятствие");

// Создаём фигуру над препятствием
shape.x = 3;
shape.y = 0;

console.log("Фигура:", shape.shapeName);

// Опускаем фигуру до столкновения
while (shape.moveDown(field)) {
    // Фигура движется вниз
}

console.log("Фигура остановилась на высоте:", shape.y);

// Закрепляем фигуру на поле
field.lockBlock(shape.getCells());

console.log("Фигура закреплена на поле");

// Проверяем количество занятых клеток
let occupiedCells = 0;

for (const row of field.grid) {
    occupiedCells += row.filter(cell => cell === 1).length;
}

console.log("Всего занятых клеток:", occupiedCells);
