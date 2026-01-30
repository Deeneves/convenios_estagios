from django import template
from core.utils.formatters import format_cpf, format_phone

register = template.Library()

@register.filter
def cpf(value):
    return format_cpf(value)

@register.filter
def phone(value):
    return format_phone(value)