from lazylist import *
import random


def quicksort(a):
    if len(a) <= 1:
        return a
    p, xs = a[0], a[1:]
    l, g = xs.partition(lambda x: x < p)
    return l.call(quicksort) + make_lazylist([p]) + g.call(quicksort)


a = list(range(100))
random.shuffle(a)
print(quicksort(make_lazylist(a)))
