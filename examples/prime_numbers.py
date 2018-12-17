from lazylist import *


def prims(l):
    p, xs = l[0], l[1:]
    return make_lazylist([p]) + xs.filter(lambda x: x % p != 0).call(prims)


print(naturals[2:].call(prims).take(100))
