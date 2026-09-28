import json
from pathlib import Path
from .config import DATA_DIR


def save_comic(comic_id: str, payload: dict):
    (DATA_DIR / f"{comic_id}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_comic(comic_id: str):
    path = DATA_DIR / f"{comic_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
