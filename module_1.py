from fastapi import HTTPException, status

# Convert char to value, skipping I and O
def char_to_value(c):
    c = c.upper()
    if c.isdigit():
        return ord(c) - ord('0')
    if c in ('I', 'O'):
        return -1
    value = ord(c) - ord('A') + 10
    if c > 'H':
        value -= 1
    if c > 'N':
        value -= 1
    return value

# Convert value to char, skipping I and O
def value_to_char(val):
    if val < 10:
        return chr(ord('0') + val)
    letters = ['A','B','C','D','E','F','G','H','J','K',
               'L','M','N','P','Q','R','S','T']
    return letters[val - 10]

# Validate number in a base (2-20), allows 1 '.' and optional '-'
def is_valid_number(num: str, base: int) -> bool:
    if base < 2 or base > 20:
        return False

    decimal_point_seen = False
    i = 0

    if num.startswith('-'):
        i += 1

    while i < len(num):
        c = num[i].upper()
        if c == '.':
            if decimal_point_seen:
                return False
            decimal_point_seen = True
            i += 1
            continue

        if c in ('I', 'O'):
            return False

        if c.isdigit():
            value = int(c)
        else:
            value = ord(c) - ord('A') + 10
            if c > 'H':
                value -= 1
            if c > 'N':
                value -= 1

        if value >= base:
            return False

        i += 1

    return len(num) > 0

# Convert valid number from base to decimal (float)
def base_to_decimal(num: str, base: int) -> float:
    i = 0
    negative = False
    if num.startswith('-'):
        negative = True
        i += 1

    result = 0.0
    # integer part
    while i < len(num) and num[i] != '.':
        result = result * base + char_to_value(num[i])
        i += 1

    # fractional part
    if i < len(num) and num[i] == '.':
        i += 1

    divisor = base
    while i < len(num):
        result += char_to_value(num[i]) / divisor
        divisor *= base
        i += 1

    return -result if negative else result

# Convert decimal float to target base string (up to 6 fractional digits)
def decimal_to_base(num: float, base: int) -> str:
    output = ''
    if num < 0:
        output += '-'
        num = -num

    int_part = int(num)
    frac_part = num - int_part

    # integer part
    if int_part == 0:
        output += '0'
    else:
        int_buffer = ''
        while int_part > 0:
            remainder = int_part % base
            int_buffer = value_to_char(remainder) + int_buffer
            int_part //= base
        output += int_buffer

    # fractional part
    if frac_part > 0:
        output += '.'
        for _ in range(6):
            frac_part *= base
            digit = int(frac_part)
            output += value_to_char(digit)
            frac_part -= digit
            if frac_part < 1e-12:
                break

    return output

def baseConverter(data):
    
    num = data.number
    base1 = int(data.from_base)
    base2 = int(data.to_base)

    if not is_valid_number(num, base1):
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="Entered number is not comatible with base")

    decimal_value = base_to_decimal(num, base1)
    result = decimal_to_base(decimal_value, base2)
    return result
