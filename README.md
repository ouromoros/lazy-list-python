# lazylist 
[![Build Status](https://travis-ci.com/ouromoros/lazy-list-python.svg?branch=master)](https://travis-ci.com/ouromoros/lazy-list-python)
[![codecov](https://codecov.io/gh/ouromoros/lazy-list-python/branch/master/graph/badge.svg)](https://codecov.io/gh/ouromoros/lazy-list-python)

Haskell-like lazy list in Python.

[Documentation](https://lazy-list-python.readthedocs.io/en/latest/index.html)

## Example
### Simple demonstration
```python
>>> from lazylist import *
>>> a = make_lazylist([1,2,5,6,8,9])
>>> print(a)
[1, 2, 5, 6, 8, 9]
>>> b = a.reverse()
>>> print(b)
[9, 8, 6, 5, 2, 1]
>>> c = a.filter(lambda x: x % 2 == 0)
>>> print(c)
[2, 6, 8]
>>> d = a.map(lambda x: x ** 2)
>>> print(d)
[1, 4, 25, 36, 64, 81]
```

### quicksort algorithm

```python
def quicksort(a):
    if len(a) <= 1:
        return a
    p, xs = a[0], a[1:]
    lesser, greater = xs.partition(lambda x: x < p)
    return lesser.call(quicksort) + make_lazylist([p]) + greater.call(quicksort)
```

### prime numbers

```python
def prims(a):
    p, xs = a[0], a[1:]
    return make_lazylist([p]) + xs.filter(lambda x: x % p != 0).call(prims)

pgen = prims(naturals[2:])
```
