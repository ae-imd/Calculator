

HEX_DIGITS: str = "0123456789ABCDEF"

def dec_to_bin(num: int) -> str:
    if num < 0:
        raise ValueError("The number must be positive integer")
    
    res: str = ""
    while num > 0:
        res = str(num % 2) + res
        num //= 2
    return res

def dec_to_oct(num: int) -> str:
    if num < 0:
        raise ValueError("The number must be positive integer")

    res: str = ""
    while num > 0:
        res = str(num % 8) + res
        num //= 8
    return res

def dec_to_hex(num: int) -> str:
    if num < 0:
        raise ValueError("The number must be positive integer")
    
    res: str = ""
    while num > 0:
        res = HEX_DIGITS[num % 16] + res
        num //= 16
    return res