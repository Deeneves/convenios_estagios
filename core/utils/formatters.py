import re
from datetime import timedelta

def format_cpf(value: str) -> str:
    if not value:
        return ""
    digits = re.sub(r"\D", "", value)
    if len(digits) != 11:
        return value
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"


def format_phone(value: str) -> str:
    if not value:
        return ""
    digits = re.sub(r"\D", "", value)

    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    elif len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return value

def format_duracao_horas(valor: timedelta) -> str:
    if not valor:
        return "—"
    total_seconds = int(valor.total_seconds())
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    segundos = total_seconds % 60
    return f"{horas}:{minutos:02d}:{segundos:02d}"