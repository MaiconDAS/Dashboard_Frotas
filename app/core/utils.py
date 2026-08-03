from __future__ import annotations

import re
from datetime import datetime, time, timedelta
from typing import Optional, Tuple


# Padrões comuns no Brasil:
# - Antigo: ABC-1234
# - Mercosul: ABC1D23
PLATE_RE = re.compile(r"^(?:[A-Z]{3}-?\d{4}|[A-Z]{3}\d[A-Z]\d{2})$")


def normalize_plate(value: str) -> str:
    v = (value or "").strip().upper()
    v = v.replace(" ", "")
    return v


def is_valid_plate(value: str) -> bool:
    v = normalize_plate(value)
    return bool(PLATE_RE.match(v))


def clamp_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    try:
        return int(s)
    except Exception:
        return None


def start_of_day(dt: datetime) -> datetime:
    return datetime.combine(dt.date(), time.min)


def end_of_day(dt: datetime) -> datetime:
    return datetime.combine(dt.date(), time.max)


def previous_week_monday_to_sunday(now: Optional[datetime] = None) -> Tuple[datetime, datetime]:
    """
    Semana anterior: segunda (00:00) até domingo (23:59:59).
    """
    now = now or datetime.now()
    today = now.date()
    # segunda=0 ... domingo=6
    this_monday = today - timedelta(days=today.weekday())
    prev_monday = this_monday - timedelta(days=7)
    prev_sunday = this_monday - timedelta(days=1)
    start = datetime.combine(prev_monday, time.min)
    end = datetime.combine(prev_sunday, time.max)
    return start, end

