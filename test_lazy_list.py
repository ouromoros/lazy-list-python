from lazy_list import *
import random


def test_consts():
    z = zeros
    for i in range(1000):
        j = random.randint(0, 1000)
        assert z[j] == 0
    o = ones
    for i in range(1000):
        j = random.randint(0, 1000)
        assert o[j] == 1
    n = naturals
    for i in range(1000):
        j = random.randint(0, 1000)
        assert n[j] == j


def test_basic():
    l = [2, 5, 6, 7, 9]
    a = make_lazy_list(l)
    assert len(a) == 5
    for i in range(len(a)):
        assert a[i] == l[i]
    b = a.map(lambda x: x * 2)
    assert len(a) == len(b)
    for i in range(len(b)):
        assert b[i] == a[i] * 2
    c = a.filter(lambda x: x % 2 == 0)
    l2 = [2, 6]
    assert c.to_list() == l2
