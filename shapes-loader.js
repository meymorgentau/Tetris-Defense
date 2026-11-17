
const fs = require("fs");
const path = require("path");

const SHAPES_FILE = path.join(__dirname, "shapes.cfg");

// Загрузка масок фигур из файла
function loadShapes(filePath = SHAPES_FILE) {
    const shapes = {};
    let currentName = null;
    let currentRows = [];

    function saveShape(name, rows) {
        if (!name || rows.length === 0) {
            throw new Error("Обнаружена фигура без маски.");
        }

        const width = rows[0].length;

        if (width === 0) {
            throw new Error(`Фигура '${name}' имеет пустую маску.`);
        }

        for (const row of rows) {
            if (row.length !== width) {
                throw new Error(
                    `Фигура '${name}': строки маски имеют разную длину.`
                );
            }

            if (!/^[01]+$/.test(row)) {
                throw new Error(
                    `Фигура '${name}': разрешены только символы 0 и 1.`
                );
            }
        }

        const cells = [];

        for (let y = 0; y < rows.length; y++) {
            for (let x = 0; x < rows[y].length; x++) {
                if (rows[y][x] === "1") {
                    cells.push([x, y]);
                }
            }
        }

        if (cells.length === 0) {
            throw new Error(
                `Фигура '${name}' не содержит ни одного кубика.`
            );
        }

        if (Object.hasOwn(shapes, name)) {
            throw new Error(`Имя фигуры '${name}' повторяется.`);
        }

        shapes[name] = cells;
    }

    let content;

    try {
        content = fs.readFileSync(filePath, "utf8");
    } catch (error) {
        if (error.code === "ENOENT") {
            throw new Error(`Файл с масками фигур не найден: ${filePath}`);
        }

        throw error;
    }

    const lines = content.split(/\r?\n/);

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        // Пропускаем пустые строки и комментарии
        if (!line || line.startsWith("#")) {
            continue;
        }

        // Заголовок новой фигуры
        if (line.startsWith("[") && line.endsWith("]")) {
            if (currentName !== null) {
                saveShape(currentName, currentRows);
            }

            currentName = line.slice(1, -1).trim();
            currentRows = [];

            if (!currentName) {
                throw new Error(
                    `Строка ${i + 1}: имя фигуры не указано.`
                );
            }

            continue;
        }

        if (currentName === null) {
            throw new Error(
                `Строка ${i + 1}: маска находится до заголовка фигуры.`
            );
        }

        if (!/^[01]+$/.test(line)) {
            throw new Error(
                `Строка ${i + 1}: разрешены только символы 0 и 1.`
            );
        }

        currentRows.push(line);
    }

    // Сохраняем последнюю фигуру
    if (currentName !== null) {
        saveShape(currentName, currentRows);
    }

    if (Object.keys(shapes).length === 0) {
        throw new Error("Файл shapes.cfg не содержит ни одной фигуры.");
    }

    return shapes;
}

module.exports = loadShapes;
