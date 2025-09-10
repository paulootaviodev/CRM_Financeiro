import random

def generate_cpf() -> str:
    """
    Generates a valid Brazilian CPF number.

    A valid CPF consists of 9 base digits and 2 verification digits.
    The verification digits are calculated based on the first 9 digits.
    """

    # Generate the first 9 random digits of the CPF
    cpf_base = [random.randint(0, 9) for _ in range(9)]

    # --- Calculation of the first verification digit (the 10th digit) ---
    
    # The weight for the first digit calculation starts from 10 and decreases to 2.
    # The sum is the sum of each digit multiplied by its weight.
    total = sum(cpf_base[i] * (10 - i) for i in range(9))

    # The first verification digit is calculated based on the remainder of the total
    # when divided by 11.
    remainder = total % 11
    first_digit = 0 if remainder < 2 else 11 - remainder

    # Add the first verification digit to the list of digits
    cpf_base.append(first_digit)

    # --- Calculation of the second verification digit (the 11th digit) ---

    # The weight for the second digit calculation starts from 11 and decreases to 2.
    # The sum now includes the first verification digit.
    total = sum(cpf_base[i] * (11 - i) for i in range(10))
    
    # The second verification digit is calculated similarly to the first.
    remainder = total % 11
    second_digit = 0 if remainder < 2 else 11 - remainder
    
    # Add the second verification digit to the list
    cpf_base.append(second_digit)
    
    # Format the CPF string with the standard mask (xxx.xxx.xxx-xx)
    cpf_str = ''.join(map(str, cpf_base))
    formatted_cpf = (
        f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
    )

    return formatted_cpf

if __name__ == "__main__":
    generated_cpf = generate_cpf()
    print(f"Generated valid CPF: {generated_cpf}")
