ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'


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
    Why use such a complicated way to generate short link paths?
    1) identifier given to the new entity in a database is unique in terms of this application
    2) a decimal number corresponds to one and only one number in any other base numeral system
    3) base 64 is derived from the fact that we use 64 characters to construct our shortened links
    So, each identifier corresponds to a unique sequence of base 64 numerals, which in turn are matched to a predetermined
    alphabet
    Transforms an integer into a sequence of symbols usable as a path in a URL. 
    """""
    as_base_64_numeral: list[int] = _decimal_to_base_64_number(identifier)
    result: str = ''
    for digit in as_base_64_numeral:
        result = result + ALPHABET[digit]
    return result


def _base_64_to_decimal(base_64_digits: list[int]) -> int:
    """AGAIN, not to be confused with Base64 encoding"""
    result: int = 0
    for idx, digit in enumerate(reversed(base_64_digits)):
        result = result + digit * 64 ** idx

    return result


def path_to_id(path: str) -> int:
    """Transforms a path of a short link into a decimal id (inverse of id_to_path). Raises ValueError if
    there are symbols not from the alphabet encountered"""
    base_64_digits = []
    for char in path:
        base_64_digits.append(ALPHABET.index(char))
    return _base_64_to_decimal(base_64_digits)

