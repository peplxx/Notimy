from random import randint
from string import ascii_uppercase, digits

CODE_ALPHABET = ascii_uppercase+digits
CODE_LENGTH = 5

def generate_code() -> str:
    return ''.join([CODE_ALPHABET[randint(0, len(CODE_ALPHABET)) - 1]
                    for _ in range(CODE_LENGTH)])
