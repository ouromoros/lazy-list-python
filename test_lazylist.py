from lazylist import *
import random
import pytest


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
    a = make_lazylist(l)
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
    with pytest.raises(IndexError):
        c[2]

def test_iter():
    l = [2, 5, 6, 7, 9]
    a = make_lazylist(l)
    for i, x in enumerate(a):
        assert l[i] == x

def test_inf():
    a = naturals
    b = naturals.map(lambda x: x * 2 + 1)
    for i in range(1000):
        j = random.randint(0, 1000)
        assert b[j] == j * 2 + 1

def test_add():
    l1 = [0, 2, 4]
    l2 = [5, 6, 7]
    a = make_lazylist(l1)
    b = make_lazylist(l2)
    c = a + b
    assert c.to_list() == l1 + l2

def test_reverse():
    pass

def test_append():
    pass

def test_take():
    pass

def test_zip():
    pass

def test_elem_index():
    pass
