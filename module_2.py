# ================= module_2.py =================
#  All functions below perform arithmetic **without converting
#  whole binary strings to integers**.

# --------------------------------------------------
# 0.  Low-level binary helpers (string-only)
# --------------------------------------------------
def _binary_compare(a: str, b: str) -> int:
    a, b = a.zfill(len(b)), b.zfill(len(a))
    for ca, cb in zip(a, b):
        if ca < cb: return -1
        if ca > cb: return 1
    return 0

def _is_zero(b: str) -> bool:
    return all(ch == '0' for ch in b)

def _left_shift(b: str, sh: int, w: int) -> str:
    if sh >= w:
        return '0' * w
    return (b + '0' * sh)[-w:]

def _add_no_overflow(a: str, b: str, w: int) -> str:
    res = ['0'] * w
    carry = 0
    for i in range(w - 1, -1, -1):
        s = int(a[i]) + int(b[i]) + carry
        res[i] = str(s & 1)
        carry = s >> 1
    return ''.join(res)

# --------------------------------------------------
# 1.  Unsigned
# --------------------------------------------------
def binary_addition(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    res = ['0'] * w
    carry = 0
    for i in range(w - 1, -1, -1):
        s = int(a[i]) + int(b[i]) + carry
        res[i] = str(s & 1)
        carry = s >> 1
    if carry:
        raise ValueError('Overflow')
    return ''.join(res)

def binary_subtraction(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    if _binary_compare(b, a) > 0:
        raise ValueError('Underflow')
    res = ['0'] * w
    borrow = 0
    for i in range(w - 1, -1, -1):
        diff = int(a[i]) - int(b[i]) - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        res[i] = str(diff)
    return ''.join(res)

def binary_multiplication(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    prod = '0' * (2 * w)
    ext = '0' * w + a
    for i in range(w):
        if b[w - 1 - i] == '1':
            shifted = _left_shift(ext, i, 2 * w)
            prod = _add_no_overflow(prod, shifted, 2 * w)
    return prod

def binary_division(a: str, b: str, w: int) -> tuple[str, str]:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    if _is_zero(b):
        raise ValueError('Division by zero')
    rem = '0' * w
    quo = '0' * w
    for i in range(w):
        rem = rem[1:] + a[i]
        if _binary_compare(rem, b) >= 0:
            rem = binary_subtraction(rem, b, w)
            quo = quo[:i] + '1' + quo[i + 1:]
    return quo, rem

# --------------------------------------------------
# 2.  Sign-magnitude
# --------------------------------------------------
def signed_binary_addition(a: str, b: str, w: int) -> str:
    if w < 2 or len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    sa, ma = a[0], a[1:]
    sb, mb = b[0], b[1:]
    if sa == sb:
        try:
            mag = binary_addition(ma, mb, w - 1)
            return sa + mag
        except ValueError:
            raise ValueError('Signed magnitude overflow')
    else:
        cmp = _binary_compare(ma, mb)
        if cmp > 0:
            return sa + binary_subtraction(ma, mb, w - 1)
        elif cmp < 0:
            return sb + binary_subtraction(mb, ma, w - 1)
        else:
            return '0' * w

def signed_binary_subtraction(a: str, b: str, w: int) -> str:
    inv_sign = '0' if b[0] == '1' else '1'
    b_neg = inv_sign + b[1:]
    return signed_binary_addition(a, b_neg, w)

def signed_binary_multiplication(a: str, b: str, w: int) -> str:
    if w < 2 or len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    sa, ma = a[0], a[1:]
    sb, mb = b[0], b[1:]
    mag_prod = binary_multiplication(ma, mb, w - 1)[-(2 * w - 1):]
    sign = '1' if sa != sb else '0'
    return sign + mag_prod

def signed_binary_division(a: str, b: str, w: int) -> tuple[str, str]:
    if w < 2 or len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    sa, ma = a[0], a[1:]
    sb, mb = b[0], b[1:]
    if _is_zero(mb):
        raise ValueError('Division by zero')
    q, r = binary_division(ma, mb, w - 1)
    q_sign = '1' if sa != sb else '0'
    r_sign = sa
    return q_sign + q, r_sign + r

# --------------------------------------------------
# 3.  1's complement
# --------------------------------------------------
def ones_complement_addition(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    s = ['0'] * w
    carry = 0
    for i in range(w - 1, -1, -1):
        t = int(a[i]) + int(b[i]) + carry
        s[i] = str(t & 1)
        carry = t >> 1
    if carry:
        one = '0' * (w - 1) + '1'
        s = list(_add_no_overflow(''.join(s), one, w))
    # overflow check: same-sign operands, opposite-sign result
    if a[0] == b[0] and s[0] != a[0]:
        raise ValueError('1\'s complement overflow')
    return ''.join(s)

def ones_complement_subtraction(a: str, b: str, w: int) -> str:
    b_inv = ''.join('1' if c == '0' else '0' for c in b)
    return ones_complement_addition(a, b_inv, w)

def ones_complement_multiplication(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    ma = a[1:] if a[0] == '0' else ''.join('1' if c == '0' else '0' for c in a[1:])
    mb = b[1:] if b[0] == '0' else ''.join('1' if c == '0' else '0' for c in b[1:])
    mag = binary_multiplication(ma, mb, w - 1)[-(2 * w - 1):]
    sign = '1' if a[0] != b[0] else '0'
    if sign == '1':
        mag = ''.join('1' if c == '0' else '0' for c in mag)
    return sign + mag

def ones_complement_division(a: str, b: str, w: int) -> tuple[str, str]:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    if _is_zero(b) or b == '1' * w:
        raise ValueError('Division by zero')
    ma = a[1:] if a[0] == '0' else ''.join('1' if c == '0' else '0' for c in a[1:])
    mb = b[1:] if b[0] == '0' else ''.join('1' if c == '0' else '0' for c in b[1:])
    q, r = binary_division(ma, mb, w - 1)
    q_sign = '1' if a[0] != b[0] else '0'
    r_sign = a[0]
    if q_sign == '1':
        q = ''.join('1' if c == '0' else '0' for c in q)
    if r_sign == '1':
        r = ''.join('1' if c == '0' else '0' for c in r)
    return q_sign + q, r_sign + r

# --------------------------------------------------
# 4.  2's complement
# --------------------------------------------------
def _twos_neg(v: str, w: int) -> str:
    inv = ''.join('1' if c == '0' else '0' for c in v)
    one = '0' * (w - 1) + '1'
    return _add_no_overflow(inv, one, w)

def twos_complement_addition(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    s = ['0'] * w
    carry = 0
    for i in range(w - 1, -1, -1):
        t = int(a[i]) + int(b[i]) + carry
        s[i] = str(t & 1)
        carry = t >> 1
    # overflow if same-sign operands, opposite-sign result
    if a[0] == b[0] and s[0] != a[0]:
        raise ValueError('2\'s complement overflow')
    return ''.join(s)

def twos_complement_subtraction(a: str, b: str, w: int) -> str:
    if b == '1' + '0' * (w - 1):
        raise ValueError('2\'s complement subtraction error')
    b_neg = _twos_neg(b, w)
    return twos_complement_addition(a, b_neg, w)

def twos_complement_multiplication(a: str, b: str, w: int) -> str:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    neg_a = a[0] == '1'
    neg_b = b[0] == '1'
    abs_a = a if not neg_a else _twos_neg(a, w)
    abs_b = b if not neg_b else _twos_neg(b, w)
    prod = binary_multiplication(abs_a, abs_b, w)
    if neg_a ^ neg_b:
        prod = _twos_neg(prod, 2 * w)
    return prod

def twos_complement_division(a: str, b: str, w: int) -> tuple[str, str]:
    if len(a) != w or len(b) != w or set(a + b) - {'0', '1'}:
        raise ValueError('Bad input')
    if _is_zero(b):
        raise ValueError('Division by zero')
    if a == '1' + '0' * (w - 1) and b == '1' * w:
        raise ValueError('2\'s complement division overflow')
    neg_a = a[0] == '1'
    neg_b = b[0] == '1'
    abs_a = a if not neg_a else _twos_neg(a, w)
    abs_b = b if not neg_b else _twos_neg(b, w)
    q, r = binary_division(abs_a, abs_b, w)
    if neg_a ^ neg_b and not _is_zero(q):
        q = _twos_neg(q, w)
    if neg_a and not _is_zero(r):
        r = _twos_neg(r, w)
    return q, r