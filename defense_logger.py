
import logging
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parent / "defense.log"

logger = logging.getLogger("defense")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log_cleared_line(row_index):
    """Записывает индекс уничтоженной строки в журнал."""
    logger.info("Уничтожена строка с индексом %s", row_index)
