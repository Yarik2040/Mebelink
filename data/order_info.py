from random import randint


def save_info(db):
    s = ''
    cnt = 0
    for elem in db:
        s += f' {db[elem]["id"]},{db[elem]["amount"]}'
        db[elem]["total"] = int("".join(db[elem]["total"].split()))
        cnt += db[elem]['total']
    s = s[1::] + f';{cnt}:{randint(1000000, 9999999)}'
    return s


def get_info(s):
    db = dict()
    db["mass"] = []
    db["id"] = s.split(':')[-1]
    s = s.split(':')[0]
    db["total"] = s.split(';')[-1]
    s = s.split(';')[0]
    mass = s.split()
    for elem in mass:
        a, b = elem.split(',')
        db["mass"].append((a, b))
    return db

