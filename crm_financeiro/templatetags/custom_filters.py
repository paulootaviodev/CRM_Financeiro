from django import template

# Create a Library instance to register custom filters
register = template.Library()

@register.filter
def format_cpf(value):
    """
    Formats a string or number as a Brazilian CPF.

    Parameters:
        value (str or int): The CPF number to format.

    Returns:
        str: CPF formatted as XXX.XXX.XXX-XX.
    """
    value = ''.join(filter(str.isdigit, str(value)))
    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}"

@register.filter
def format_phone(value):
    """
    Formats a string or number as a Brazilian phone number.

    Parameters:
        value (str or int): The phone number to format.

    Returns:
        str: Phone formatted as (XX)XXXXX-XXXX or (XX)XXXX-XXXX,
             depending on length. Returns original value if not valid.
    """
    value = ''.join(filter(str.isdigit, str(value)))
    if len(value) == 11:
        return f"({value[:2]}){value[2:7]}-{value[7:]}"
    elif len(value) == 10:
        return f"({value[:2]}){value[2:6]}-{value[6:]}"
    return value

@register.filter(name='format_currency')
def format_currency(value):
    """
    Formats a numeric value as Brazilian currency (R$).

    Parameters:
        value (float or int): The monetary value to format.

    Returns:
        str: Value formatted as 'R$ X.XXX,XX' using Brazilian notation.
    """
    value = f"R$ {float(value):,.2f}" \
        .replace(",", "X") \
        .replace(".", ",") \
        .replace("X", ".")
    return value
