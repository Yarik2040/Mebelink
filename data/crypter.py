def crypt(s):
    alpha = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    n = len(s)
    res = ''
    for c in s:
        res += alpha[(alpha.index(c) + n) % len(alpha)]
    return res


def decrypt(s):
    alpha = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha = alpha[::-1]
    n = len(s)
    res = ''
    for c in s:
        res += alpha[(alpha.index(c) + n) % len(alpha)]
    return res
