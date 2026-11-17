
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreElement = document.getElementById("score");
const pauseButton = document.getElementById("pauseButton");
const restartButton = document.getElementById("restartButton");

// Размеры игрового поля
const CELL_SIZE = 30;
const GRID_WIDTH = 10;
const GRID_HEIGHT = 20;

// Скорость падения
const FALL_SPEED = 120;

// Игровое поле
const grid = Array.from(
    { length: GRID_HEIGHT },
    () => Array(GRID_WIDTH).fill(null)
);

// Пушка
const cannon = {
    x: 130,
    y: 564,
    width: 40,
    height: 16,
    speed: 260
};

// Состояние клавиш
const keys = {
    a: false,
    d: false
};

// Игровые объекты
const bullets = [];

// Состояние игры
let currentShape = null;
let score = 0;
let gameOver = false;
let paused = false;
let lastTime = 0;

// Фигуры
const shapes = [
    {
        name: "O",
        cells: [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]],
        color: "#ff96c8"
    },
    {
        name: "I",
        cells: [[0, 0], [1, 0], [2, 0], [3, 0]],
        color: "#b464ff"
    },
    {
        name: "T",
        cells: [[0, 0], [1, 0], [2, 0], [1, 1]],
        color: "#50b4ff"
    },
    {
        name: "L",
        cells: [[0, 0], [0, 1], [0, 2], [1, 2]],
        color: "#dc8cff"
    },
    {
        name: "Square",
        cells: [[0, 0], [1, 0], [0, 1], [1, 1]],
        color: "#ffdc50"
    }
];

// Создание фигуры
function createShape() {
    const template = shapes[
        Math.floor(Math.random() * shapes.length)
    ];

    const cells = template.cells.map(cell => [...cell]);

    const shapeWidth = Math.max(
        ...cells.map(cell => cell[0])
    ) + 1;

    const shape = {
        name: template.name,
        cells: cells,
        color: template.color,
        x: Math.floor(Math.random() * (GRID_WIDTH - shapeWidth + 1)),
        y: 0
    };

    if (!canPlaceShape(shape, shape.y)) {
        gameOver = true;
        currentShape = null;
        return;
    }

    currentShape = shape;
}

// Проверка возможности размещения фигуры
function canPlaceShape(shape, newY) {
    for (const [cellX, cellY] of shape.cells) {
        const column = shape.x + cellX;

        const row = Math.floor(
            (newY + cellY * CELL_SIZE) / CELL_SIZE
        );

        if (column < 0 || column >= GRID_WIDTH) {
            return false;
        }

        if (row < 0 || row >= GRID_HEIGHT) {
            return false;
        }

        if (grid[row][column] !== null) {
            return false;
        }
    }

    return true;
}

// Закрепление фигуры на поле
function lockShape() {
    if (!currentShape) return;

    for (const [cellX, cellY] of currentShape.cells) {
        const column = currentShape.x + cellX;

        const row = Math.floor(
            currentShape.y / CELL_SIZE
        ) + cellY;

        if (
            row >= 0 && row < GRID_HEIGHT &&
            column >= 0 && column < GRID_WIDTH
        ) {
            grid[row][column] = currentShape.color;
        }
    }

    currentShape = null;

    clearFullLines();
    createShape();
}

// Удаление заполненных линий
function clearFullLines() {
    let cleared = 0;

    for (let row = GRID_HEIGHT - 1; row >= 0; row--) {
        if (grid[row].every(cell => cell !== null)) {
            grid.splice(row, 1);
            grid.unshift(Array(GRID_WIDTH).fill(null));

            cleared++;
            row++;
        }
    }

    if (cleared > 0) {
        score += cleared * 100;
        updateScore();
    }
}

// Обновление счёта
function updateScore() {
    scoreElement.textContent = score;
}

// Движение пушки
function updateCannon(deltaTime) {
    if (keys.a) {
        cannon.x -= cannon.speed * deltaTime;
    }

    if (keys.d) {
        cannon.x += cannon.speed * deltaTime;
    }

    cannon.x = Math.max(
        0,
        Math.min(canvas.width - cannon.width, cannon.x)
    );
}

// Создание пули
function shoot() {
    if (gameOver || paused) return;

    bullets.push({
        x: cannon.x + cannon.width / 2 - 3,
        y: cannon.y - 12,
        width: 6,
        height: 12,
        speed: 450
    });
}

// Проверка столкновения прямоугольников
function intersects(a, b) {
    return (
        a.x < b.x + b.width &&
        a.x + a.width > b.x &&
        a.y < b.y + b.height &&
        a.y + a.height > b.y
    );
}

// Обновление пуль
function updateBullets(deltaTime) {
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];

        bullet.y -= bullet.speed * deltaTime;

        let bulletHit = false;

        // Пули взаимодействуют только с падающей фигурой.
        // Закреплённые кубики на игровом поле не разрушаются.
        if (currentShape) {
            for (
                let j = currentShape.cells.length - 1;
                j >= 0;
                j--
            ) {
                const [cellX, cellY] = currentShape.cells[j];

                const cellRect = {
                    x: (currentShape.x + cellX) * CELL_SIZE,
                    y: currentShape.y + cellY * CELL_SIZE,
                    width: CELL_SIZE,
                    height: CELL_SIZE
                };

                if (intersects(bullet, cellRect)) {
                    destroyCell(j);
                    bulletHit = true;
                    break;
                }
            }
        }

        if (
            bulletHit ||
            bullet.y + bullet.height < 0
        ) {
            bullets.splice(i, 1);
        }
    }
}

// Разрушение кубика падающей фигуры
function destroyCell(index) {
    if (!currentShape) return;

    currentShape.cells.splice(index, 1);

    score += 10;
    updateScore();

    // Если все кубики уничтожены
    if (currentShape.cells.length === 0) {
        currentShape = null;
        createShape();
    }
}

// Плавное падение фигуры
function updateShape(deltaTime) {
    if (!currentShape) return;

    const nextY = currentShape.y + FALL_SPEED * deltaTime;

    if (canPlaceShape(currentShape, nextY)) {
        currentShape.y = nextY;
    } else {
        currentShape.y =
            Math.floor(currentShape.y / CELL_SIZE) * CELL_SIZE;

        lockShape();
    }
}

// Отрисовка сетки
function drawGrid() {
    ctx.strokeStyle = "#29364d";
    ctx.lineWidth = 1;

    for (let column = 0; column <= GRID_WIDTH; column++) {
        ctx.beginPath();
        ctx.moveTo(column * CELL_SIZE, 0);
        ctx.lineTo(column * CELL_SIZE, canvas.height);
        ctx.stroke();
    }

    for (let row = 0; row <= GRID_HEIGHT; row++) {
        ctx.beginPath();
        ctx.moveTo(0, row * CELL_SIZE);
        ctx.lineTo(canvas.width, row * CELL_SIZE);
        ctx.stroke();
    }
}

// Отрисовка закреплённых кубиков
function drawLockedBlocks() {
    for (let row = 0; row < GRID_HEIGHT; row++) {
        for (let column = 0; column < GRID_WIDTH; column++) {
            if (grid[row][column] !== null) {
                ctx.fillStyle = grid[row][column];

                ctx.fillRect(
                    column * CELL_SIZE + 1,
                    row * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                );
            }
        }
    }
}

// Отрисовка падающей фигуры
function drawShape() {
    if (!currentShape) return;

    ctx.fillStyle = currentShape.color;

    for (const [cellX, cellY] of currentShape.cells) {
        ctx.fillRect(
            (currentShape.x + cellX) * CELL_SIZE + 1,
            currentShape.y + cellY * CELL_SIZE + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2
        );
    }
}

// Отрисовка пушки
function drawCannon() {
    ctx.fillStyle = "#80cfff";

    ctx.fillRect(
        cannon.x,
        cannon.y,
        cannon.width,
        cannon.height
    );

    ctx.fillStyle = "#ffffff";

    ctx.fillRect(
        cannon.x + 16,
        cannon.y - 12,
        8,
        12
    );
}

// Отрисовка пуль
function drawBullets() {
    ctx.fillStyle = "#ffffff";

    for (const bullet of bullets) {
        ctx.fillRect(
            bullet.x,
            bullet.y,
            bullet.width,
            bullet.height
        );
    }
}

// Сообщение о паузе
function drawPause() {
    if (!paused) return;

    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#80cfff";
    ctx.font = "bold 30px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        "ПАУЗА",
        canvas.width / 2,
        canvas.height / 2
    );
}

// Сообщение о завершении игры
function drawGameOver() {
    if (!gameOver) return;

    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#ff7777";
    ctx.font = "bold 28px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        "GAME OVER",
        canvas.width / 2,
        canvas.height / 2
    );

    ctx.fillStyle = "#ffffff";
    ctx.font = "14px Arial";

    ctx.fillText(
        "Нажми «Начать заново»",
        canvas.width / 2,
        canvas.height / 2 + 35
    );
}

// Отрисовка всей игры
function drawGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawGrid();
    drawLockedBlocks();
    drawShape();
    drawCannon();
    drawBullets();

    drawPause();
    drawGameOver();
}

// Переключение паузы
function togglePause() {
    if (gameOver) return;

    paused = !paused;

    pauseButton.textContent = paused
        ? "Продолжить"
        : "Пауза";

    // Сбрасываем время кадра, чтобы после паузы
    // игра не пыталась обработать накопившееся время.
    lastTime = 0;
}

// Перезапуск игры
function restartGame() {
    for (let row = 0; row < GRID_HEIGHT; row++) {
        grid[row].fill(null);
    }

    bullets.length = 0;

    cannon.x = 130;

    score = 0;
    gameOver = false;
    paused = false;

    keys.a = false;
    keys.d = false;

    lastTime = 0;

    updateScore();

    pauseButton.textContent = "Пауза";

    createShape();
}

// Игровой цикл
function gameLoop(timestamp) {
    const deltaTime = lastTime === 0
        ? 0
        : Math.min((timestamp - lastTime) / 1000, 0.05);

    lastTime = timestamp;

    if (!gameOver && !paused) {
        updateCannon(deltaTime);
        updateBullets(deltaTime);
        updateShape(deltaTime);
    }

    drawGame();

    requestAnimationFrame(gameLoop);
}

// Управление клавиатурой
document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();

    if (key === "a") keys.a = true;
    if (key === "d") keys.d = true;

    if (event.code === "Space") {
        event.preventDefault();

        if (!event.repeat) {
            shoot();
        }
    }

    if (key === "p" && !event.repeat) {
        togglePause();
    }

    if (key === "r" && gameOver) {
        restartGame();
    }
});

// Отпускание клавиш
document.addEventListener("keyup", (event) => {
    const key = event.key.toLowerCase();

    if (key === "a") keys.a = false;
    if (key === "d") keys.d = false;
});

// Выстрел мышью
canvas.addEventListener("click", shoot);

// Кнопки управления
pauseButton.addEventListener("click", togglePause);
restartButton.addEventListener("click", restartGame);

// Запуск игры
createShape();
requestAnimationFrame(gameLoop);
