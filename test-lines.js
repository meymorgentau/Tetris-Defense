
const GameField = require("./game-field.js");

const field = new GameField();

// Заполняем нижнюю строку девятью кубиками
const firstCells = [];

for (let column = 0; column < 9; column++) {
    firstCells.push([column, 19]);
}

field.lockBlock(firstCells);

console.log(
    "Кубики закреплены:",
    field.grid[19].filter(cell => cell === 1).length
);

// Добавляем последний кубик
field.lockBlock([[9, 19]]);

console.log(
    "Строка заполнена:",
    field.grid[19].every(cell => cell === 1)
);

// Удаляем заполненную строку
const result = field.clearFullLines();

console.log("Удалено линий:", result.clearedLines);
console.log("Индексы удалённых строк:", result.clearedRowIndices);

console.log(
    "Нижняя строка после очистки:",
    field.grid[19]
);
