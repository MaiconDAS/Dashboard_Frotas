from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from app.core.paths import get_logs_dir


def setup_logging() -> None:
    logs_dir = get_logs_dir()
    log_file = logs_dir / "app.log"

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=2_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    console.setLevel(logging.INFO)

    root.handlers.clear()
    root.addHandler(file_handler)
    root.addHandler(console)

