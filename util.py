import math
from functools import wraps


def invert(l):
    o = [list() for _ in range(len(max(l, key=len)))]
    for i in l:
        for n, v in enumerate(i):
            o[n].append(v)
    return o


def filter_by_distance(cutoff, tuple_dist):
    out = []
    for obj, dist in tuple_dist:
        if dist <= cutoff:
            out.append(obj)
        else:
            return out
    return out


def unique(s, limit=float("inf")):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            n = 0
            while n < limit:
                result = func(*args, **kwargs)
                if result not in s:
                    s.add(result)
                    return result
                n += 1
            raise RuntimeError("Limit exceeded without finding unique value")

        return wrapped

    return wrapper


def distance(p1, p2):
    ax, ay, az = p1
    bx, by, bz = p2
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2)