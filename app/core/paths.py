from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "VehicleDashboard"


def _is_writable_dir(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test = path / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def get_data_dir() -> Path:
    """
    Regra:
    1) tenta usar uma pasta `data/` ao lado do executável/script
    2) se não for possível gravar, cai para %APPDATA%\\VehicleDashboard\\data
    """
    # Base do projeto em dev / base do executável no modo "frozen"
    if getattr(sys := __import__("sys"), "frozen", False):
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = Path(__file__).resolve().parents[2]

    candidate = base_dir / "data"
    if _is_writable_dir(candidate):
        return candidate

    appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    fallback = Path(appdata) / APP_NAME / "data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def get_db_path() -> Path:
    return get_data_dir() / "app.db"


def get_config_path() -> Path:
    return get_data_dir() / "config.json"


def get_logs_dir() -> Path:
    d = get_data_dir() / "logs"
    d.mkdir(parents=True, exist_ok=True)
    return d

