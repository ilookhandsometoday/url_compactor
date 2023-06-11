_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'


def _decimal_to_base_64_number(n: int) -> list[int]:
    """NOT TO BE CONFUSED WITH BASE64 ENCODING,
    as in this case the input is not binary data; we're simply converting from one numeral system to another
    Returns a list of base64 digits."""
    if n == 0:
        return [0]

    result = []
    while n:
        n, remainder = divmod(n, 64)
        result.insert(-2, remainder)

    return result


def id_to_path(identifier: int) -> str:
    """
    1) identifier given to the new entity in a database is unique in terms of this application
    2) a decimal number corresponds to one and only one number in any other base numeral system
    3) base 64 is derived from the fact that we use 64 characters to construct our shortened links
    """""
    as_base_64_numeral: list[int] = _decimal_to_base_64_number(identifier)
    result: str = ''
    for digit in as_base_64_numeral:
        result = result + _alphabet[digit]
    return result


def _base_64_to_decimal(base_64_digits: list[int]) -> int:
    """AGAIN, not to be confused with Base64 encoding"""
    result: int = 0
    for idx, digit in enumerate(reversed(base_64_digits)):
        result = result + digit * 64 ** idx

    return result


def path_to_id(path: str) -> int:
    base_64_digits = []
    for char in path:
        base_64_digits.append(_alphabet.index(char))
    return _base_64_to_decimal(base_64_digits)

