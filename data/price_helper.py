def better_price(n):
    s = ''
    n = str(n)
    cnt = len(n) // 3
    for i in range(1, len(n) + 1):
        s += n[len(n) - i]
        if i % 3 == 0 and cnt > 0:
            cnt -= 1
            s += ' '
    s = s[::-1]
    if s[0] == ' ':
        s = s[1:]
    return s

