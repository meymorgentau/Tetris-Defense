
from pathlib import Path


SHAPES_FILE = Path(__file__).resolve().parent / "shapes.cfg"


def load_shapes(file_path=SHAPES_FILE):
    """Загружает маски фигур из файла и преобразует их в координаты кубиков."""
    shapes = {}
    current_name = None
    current_rows = []

    def save_shape(name, rows):
        if not name or not rows:
            raise ValueError("Обнаружена фигура без маски.")

        width = len(rows[0])

        if width == 0:
            raise ValueError(f"Фигура '{name}' имеет пустую маску.")

        for row in rows:
            if len(row) != width:
                raise ValueError(
                    f"Фигура '{name}': строки маски имеют разную длину."
                )

            if any(char not in "01" for char in row):
                raise ValueError(
                    f"Фигура '{name}': разрешены только символы 0 и 1."
                )

        cells = [
            (x, y)
            for y, row in enumerate(rows)
            for x, char in enumerate(row)
            if char == "1"
        ]

        if not cells:
            raise ValueError(
                f"Фигура '{name}' не содержит ни одного кубика."
            )

        if name in shapes:
            raise ValueError(f"Имя фигуры '{name}' повторяется.")

        shapes[name] = cells

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                # Пропускаем пустые строки и комментарии.
                if not line or line.startswith("#"):
                    continue

                # Заголовок обозначает начало новой фигуры.
                if line.startswith("[") and line.endswith("]"):
                    if current_name is not None:
                        save_shape(current_name, current_rows)

                    current_name = line[1:-1].strip()
                    current_rows = []

                    if not current_name:
                        raise ValueError(
                            f"Строка {line_number}: имя фигуры не указано."
                        )

                    continue

                if current_name is None:
                    raise ValueError(
                        f"Строка {line_number}: маска находится "
                        "до заголовка фигуры."
                    )

                if any(char not in "01" for char in line):
                    raise ValueError(
                        f"Строка {line_number}: разрешены только 0 и 1."
                    )

                current_rows.append(line)

        # Сохраняем последнюю фигуру после завершения чтения файла.
        if current_name is not None:
            save_shape(current_name, current_rows)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Файл с масками фигур не найден: {file_path}"
        ) from None

    if not shapes:
        raise ValueError("Файл shapes.cfg не содержит ни одной фигуры.")

    return shapes

if __name__ == "__main__":
    try:
        loaded_shapes = load_shapes()

        for name, cells in loaded_shapes.items():
            print(f"{name}: {cells}")

        print(f"\nУспешно загружено фигур: {len(loaded_shapes)}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Ошибка загрузки фигур: {error}")