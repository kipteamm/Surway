from hashlib import sha512

from six import text_type

import secrets


def sha256(input: str) -> str:
    return sha512(text_type(input).encode()).hexdigest()


def random_string(amount: int) -> str:
    return secrets.token_hex(amount)