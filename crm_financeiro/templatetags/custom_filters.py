from django import template

register = template.Library()

@register.filter
def format_cpf(value):
    value = ''.join(filter(str.isdigit, str(value)))
    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"

@register.filter
def format_phone(value):
    value = ''.join(filter(str.isdigit, str(value)))
    if len(value) == 11:
        return f"({value[:2]}){value[2:7]}-{value[7:]}"
    elif len(value) == 10:
        return f"({value[:2]}){value[2:6]}-{value[6:]}"
    return value
