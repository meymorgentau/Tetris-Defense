
const GameField = require("./game-field.js");

const field = new GameField();

console.log("HELLO TEST:", field.width, "x", field.height);

// Занимаем несколько ячеек
field.occupyCell(19, 0);
field.occupyCell(19, 1);

console.log(
    "Ячейка (19, 0) занята:",
    field.isCellOccupied(19, 0)
);

// Проверяем размещение фигуры
const cells = [
    [2, 0],
    [3, 0],
    [4, 0]
];

console.log(
    "Можно разместить фигуру:",
    field.canPlaceBlock(cells)
);

// Заполняем нижнюю строку
for (let column = 0; column < field.width; column++) {
    field.occupyCell(19, column);
}

// Удаляем заполненные линии
const result = field.clearFullLines();

console.log("Удалено линий:", result.clearedLines);
console.log("Индексы удалённых строк:", result.clearedRowIndices);
