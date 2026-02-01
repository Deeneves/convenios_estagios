from django import template
from core.utils.formatters import format_cpf, format_phone
from datetime import timedelta

register = template.Library()

@register.filter
def cpf(value):
    return format_cpf(value)

@register.filter
def phone(value):
    return format_phone(value)

@register.filter
def duracao_horas(valor):
    if not valor:
        return "—"
    if isinstance(valor, timedelta):
        total_seconds = int(valor.total_seconds())
    else:
        try:
            total_seconds = int(valor)
        except (TypeError, ValueError):
            return valor
    if total_seconds < 0:
        total_seconds = abs(total_seconds)
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    segundos = total_seconds % 60
    return f"{horas}:{minutos:02d}:{segundos:02d}"