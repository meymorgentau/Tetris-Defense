
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SESSIONS_DIR = BASE_DIR / "sessions"


def get_session_path(user_id: int) -> Path:
    return SESSIONS_DIR / f"{user_id}.json"


def load_session(user_id: int) -> dict:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    session_path = get_session_path(user_id)

    if not session_path.exists():
        return {
            "user_id": user_id,
            "player_name": None,
            "games_played": 0,
            "lines_cleared": 0,
            "score": 0,
            "achievements": []
        }

    try:
        with open(session_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {
            "user_id": user_id,
            "player_name": None,
            "games_played": 0,
            "lines_cleared": 0,
            "score": 0,
            "achievements": []
        }


def save_session(user_id: int, data: dict) -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    session_path = get_session_path(user_id)

    with open(session_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
