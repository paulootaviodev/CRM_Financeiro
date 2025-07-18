import re

def remove_non_numeric(value: str) -> str:
    """Remove all non-numeric characters from the input string."""
    return re.sub(r'\D', '', value)

def validate_cpf(cpf: str) -> bool:
    """Validate CPF number by checking its structure and check digits."""
    if not re.fullmatch(r"\d{11}", cpf):
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    for i in range(9, 11):
        sum_digits = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        check_digit = ((sum_digits * 10) % 11) % 10

        if check_digit != int(cpf[i]):
            return False
        
    return True

def validate_email_format(email):
    """Valida o formato do e-mail usando regex."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(email_regex, email)
