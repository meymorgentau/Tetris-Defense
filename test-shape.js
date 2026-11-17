
const FallingShape = require("./falling-shape.js");

// Создаём первую фигуру
const firstShape = new FallingShape();

console.log("Первая фигура:", firstShape.shapeName);
console.log("Координаты кубиков:", firstShape.getCells());
console.log("Цвет фигуры:", firstShape.color);
console.log("Начальная позиция:", firstShape.x, firstShape.y);

// Проверяем перемещение вниз
firstShape.moveDown();

console.log("Позиция после перемещения:", firstShape.y);

// Проверяем удаление кубика
firstShape.removeCell(firstShape.shape[0]);

console.log("Количество оставшихся кубиков:", firstShape.shape.length);
console.log("Фигура уничтожена:", firstShape.isDestroyed());

// Проверяем загрузку всех фигур
console.log("Всего загружено фигур:", Object.keys(FallingShape.SHAPES).length);
console.log("Названия фигур:", Object.keys(FallingShape.SHAPES));
