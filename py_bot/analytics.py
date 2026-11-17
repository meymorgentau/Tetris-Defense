
import csv
import logging
from pathlib import Path
from datetime import datetime
from collections import Counter


# Paths to game files
BASE_DIR = Path(__file__).resolve().parent.parent
SHAPES_FILE = BASE_DIR / "shapes.cfg"
LOG_FILE = BASE_DIR / "defense.log"

# CSV leaderboard file
CSV_FILE = Path(__file__).resolve().parent / "leaderboard.csv"

logger = logging.getLogger(__name__)


def load_shapes():
    """Loads available shapes from shapes.cfg."""

    shapes = {}

    if not SHAPES_FILE.exists():
        logger.error("Shapes file not found: %s", SHAPES_FILE)
        return shapes

    try:
        with open(SHAPES_FILE, "r", encoding="utf-8") as file:
            current_shape = None
            rows = []

            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("[") and line.endswith("]"):
                    if current_shape is not None:
                        shapes[current_shape] = rows

                    current_shape = line[1:-1]
                    rows = []

                elif current_shape is not None:
                    if all(char in "01" for char in line):
                        rows.append(line)

            if current_shape is not None:
                shapes[current_shape] = rows

    except (OSError, UnicodeError) as error:
        logger.error("Error loading shapes: %s", error)

    return shapes


def analyze_log():
    """Analyzes events stored in defense.log."""

    result = {
        "total_lines": 0,
        "rows": Counter(),
        "events": [],
        "first_event": None,
        "last_event": None
    }

    if not LOG_FILE.exists():
        logger.warning("Game log file not found.")
        return result

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    date_text, event_text = line.split(" | ", 1)

                    event_date = datetime.strptime(
                        date_text,
                        "%Y-%m-%d %H:%M:%S"
                    )

                    if not event_text.startswith(
                        "Уничтожена строка с индексом "
                    ):
                        continue

                    row_index = int(event_text.rsplit(" ", 1)[1])

                    result["events"].append({
                        "date": event_date,
                        "row_index": row_index
                    })

                    result["rows"][row_index] += 1

                except (ValueError, IndexError):
                    logger.warning("Invalid log entry: %s", line)

        result["total_lines"] = len(result["events"])

        if result["events"]:
            result["first_event"] = result["events"][0]["date"]
            result["last_event"] = result["events"][-1]["date"]

    except (OSError, UnicodeError) as error:
        logger.error("Error reading game log: %s", error)

    return result


def create_leaderboard():
    """Creates CSV leaderboard if it does not exist."""

    if not CSV_FILE.exists():
        CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "player_name",
                "lines_cleared",
                "score",
                "games_played"
            ])


def load_leaderboard():
    """Loads player results from CSV."""

    create_leaderboard()
    players = []

    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    players.append({
                        "player_name": row["player_name"],
                        "lines_cleared": int(row["lines_cleared"]),
                        "score": int(row["score"]),
                        "games_played": int(row["games_played"])
                    })

                except (ValueError, KeyError, TypeError):
                    logger.warning("Invalid CSV row: %s", row)

    except (OSError, UnicodeError) as error:
        logger.error("Error reading leaderboard: %s", error)

    return players


def get_top_players(limit=10):
    """Returns players sorted by cleared lines."""

    players = load_leaderboard()

    return sorted(
        players,
        key=lambda player: player["lines_cleared"],
        reverse=True
    )[:limit]


def get_player_statistics():
    """Calculates general player statistics."""

    players = load_leaderboard()

    return {
        "players_count": len(players),
        "total_lines": sum(p["lines_cleared"] for p in players),
        "total_score": sum(p["score"] for p in players),
        "total_games": sum(p["games_played"] for p in players)
    }


def get_achievements(lines_cleared=None):
    """Returns achievements based on the best player result."""

    if lines_cleared is None:
        players = load_leaderboard()

        if not players:
            return []

        lines_cleared = max(
            player["lines_cleared"]
            for player in players
        )

    achievements = []

    if lines_cleared >= 10:
        achievements.append("🥉 Новичок: уничтожено 10 линий")

    if lines_cleared >= 50:
        achievements.append("🥈 Защитник: уничтожено 50 линий")

    if lines_cleared >= 100:
        achievements.append("🥇 Легенда: уничтожено 100 линий")

    return achievements


def import_csv(file_path):
    """Imports and validates player results from another CSV file."""

    required_columns = {
        "player_name",
        "lines_cleared",
        "score",
        "games_played"
    }

    imported_players = []

    try:
        with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                raise ValueError("CSV file has incorrect columns.")

            for row in reader:
                player_name = row["player_name"].strip()

                lines = int(row["lines_cleared"])
                score = int(row["score"])
                games = int(row["games_played"])

                if not player_name or lines < 0 or score < 0 or games < 0:
                    raise ValueError("CSV contains invalid player data.")

                imported_players.append({
                    "player_name": player_name,
                    "lines_cleared": lines,
                    "score": score,
                    "games_played": games
                })

        create_leaderboard()

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "player_name",
                    "lines_cleared",
                    "score",
                    "games_played"
                ]
            )

            writer.writerows(imported_players)

        return len(imported_players)

    except (OSError, UnicodeError, ValueError, TypeError) as error:
        logger.error("CSV import failed: %s", error)
        raise
