import re
from datetime import datetime, timedelta


def validar_placa(placa: str) -> bool:
    """Valida formato de placa brasileira (Mercosul ou antiga)."""
    if not placa:
        return False
    placa = placa.strip().upper().replace("-", "")
    padrao_antigo = re.compile(r"^[A-Z]{3}[0-9]{4}$")
    padrao_mercosul = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")
    return bool(padrao_antigo.match(placa) or padrao_mercosul.match(placa))


def is_valid_plate(placa: str) -> bool:
    """Alias para validar_placa (compatibilidade com vehicle_service)."""
    return validar_placa(placa)


def normalize_plate(placa: str) -> str:
    """Normaliza placa: maiusculas, sem hifen."""
    return placa.strip().upper().replace("-", "")


def formatar_data(data: datetime | str | None, fmt: str = "%d/%m/%Y") -> str:
    if data is None:
        return ""
    if isinstance(data, str):
        try:
            data = datetime.fromisoformat(data)
        except ValueError:
            return data
    return data.strftime(fmt)


def parse_data(data_str: str, fmt: str = "%d/%m/%Y") -> datetime | None:
    try:
        return datetime.strptime(data_str, fmt)
    except ValueError:
        return None


def previous_week_monday_to_sunday(reference_date: datetime | None = None) -> tuple[datetime, datetime]:
    """Retorna (segunda, domingo) da semana anterior a reference_date."""
    if reference_date is None:
        reference_date = datetime.now()
    days_since_sunday = reference_date.weekday() + 1
    last_sunday = reference_date - timedelta(days=days_since_sunday)
    last_monday = last_sunday - timedelta(days=6)
    monday_start = last_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    sunday_end = last_sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
    return monday_start, sunday_end
