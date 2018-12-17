"""
lazylist
=========
Haskell-like lazily evaluated list in Python.
"""
import functools
import math


def check_finite(func):
    """Raises ValueError if the annonated function is called on infinite instance"""
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self.inf:
            raise ValueError("Invalid Operation on Infinite List!")
        return func(self, *args, **kwargs)
    return wrap


def const(value):
    return lambda: value


class LazyList(object):
    """Lazily evaluated list.

    Attributes:
        func: Function that accepts `int` as index and returns the corresponding value.
            Should raise `IndexError` when out of bound.
        getsize: Function with no arguemnt and returns the supposed size. It is optional
            but should be provided when the size can be determined without evaluating all
            elements.
        inf: Bool that indicates if the list is an infinite one. When `inf` is True, there's
            no need to provide `getsize`.
    """

    def __init__(self, func, getsize=None, inf=False):
        self.func = func
        self.cache = dict()
        self.getsize = getsize
        self.inf = inf
        self.size = None

    def __len__(self):
        if self.inf:
            return 0
        if self.size:
            return self.size
        if self.getsize:
            self.size = self.getsize()
            return self.size
        # try to evaluate every element until out of bound
        i = max(self.cache.keys(), default=0)
        while True:
            try:
                self[i]
            except IndexError:
                break
            i += 1
        self.size = i
        return self.size

    def __contains__(self, item):
        return self.elem_index(item) != -1

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start or 0, key.stop or len(
                self), key.step or 1
            if not self.inf and stop:
                size = (stop - start) // step + 1
                return LazyList(lambda _, i: self[start + i * step], const(size))
            # when stop is not provided and self is infinite, result is infinite
            return LazyList(lambda _, i: self[start + i * step], inf=True)
        elif isinstance(key, int):
            if key in self.cache:
                return self.cache[key]
            self._evaluate(key)
            return self.cache[key]
        else:
            raise KeyError("Index can only be slice or integer!")

    def __str__(self):
        return str(self.to_list())

    def _evaluate(self, i):
        self.cache[i] = self.func(self, i)

    @check_finite
    def __add__(self, other):
        """Returns list with the provided list concatenated to the end."""
        def getitem(_, i):
            try:
                return self[i]
            except IndexError:
                return other[i - len(self)]

        return LazyList(getitem, lambda: len(self) + len(other), self.inf or other.inf)

    def call(self, f):
        """Returns list which is the result of applying `f` to `self`."""
        result = None
        def getitem(_, i):
            nonlocal result
            if result:
                return result[i]
            result = f(self)
            return result[i]
        return LazyList(getitem, inf=self.inf)


    @check_finite
    def to_list(self):
        """Returns corresponding Python built-in list. Raises `ValueError` if called
        on infinite list.
        """
        if self.inf:
            raise ValueError
        return [self[i] for i in range(len(self))]

    def head(self):
        return self[0]

    def last(self):
        return self[len(self) - 1]

    def tail(self):
        return LazyList(lambda _, i: self[i + 1], lambda: len(self) - 1)

    def init(self):
        pass

    def null(self):
        return len(self) == 0

    def map(self, f):
        return LazyList(lambda _, i: f(self[i]), lambda: len(self), self.inf)

    @check_finite
    def reverse(self):
        """Returns reveresed list."""
        return LazyList(lambda _, i: self[len(self) - 1 - i], lambda: len(self))

    @check_finite
    def append(self, a):
        """Returns list with the provided element appended to the end."""
        def getitem(_, i):
            if i == len(self):
                return a
            return self[i]
        return LazyList(getitem, lambda: len(self) + 1)

    def intersperse(self, x):
        pass

    def intercalate(self, x):
        pass

    def transpose(self):
        pass

    def subsequences(self):
        pass

    def permutations(self):
        pass

    def foldl(self):
        pass

    def foldr(self):
        pass

    def concat(self):
        pass

    def concat_map(self, f):
        pass

    def sum(self):
        return sum(self)

    def scanl(self):
        pass

    def scanr(self):
        pass

    def find(self, p):
        pass

    def filter(self, p):
        data = []
        last_index = 0

        def getitem(_, i):
            nonlocal data
            nonlocal last_index
            if i >= len(data):
                for _ in range(len(data), i + 1):
                    while not p(self[last_index]):
                        last_index += 1
                    data.append(self[last_index])
                    last_index += 1
            return data[i]

        return LazyList(getitem, inf=self.inf)

    def partition(self, p):
        return (self.filter(p), self.filter(lambda x: not p(x)))

    def elem_index(self, item):
        """Returns the index of corresponding element. Returns -1 if not found."""
        if self.inf:
            raise Warning(
                "Calling elemIndex on infinite list! Might run forever...")
        i = 0
        while True:
            try:
                if self[i] == item:
                    return i
            except IndexError:
                return -1
            i += 1

    def take(self, n):
        return LazyList(lambda _, i: self[i], const(n))

    def take_while(self, p, n):
        return self.filter(p).take(n)

    def splitAt(self, n):
        pass

    def drop(self, n):
        if self.size:
            size = self.size - n
        else:
            size = None
        return LazyList(lambda _, i: self[i + n], const(size), self.inf)

    def drop_while(self, n):
        pass

    def span(self, p):
        pass

    def break_(self, p):
        pass

    def group(self):
        pass

    def inits(self):
        pass

    def tails(self):
        pass

    def replicate(self, n):
        pass

    def zip(self, *args):
        pass


def make_lazylist(iterable):
    """Returns a list whose values are adapted from supplied iterable."""
    copy = list(iterable)
    return LazyList(lambda _, i: copy[i], const(len(copy)))


def repeat(item):
    """Returns an infinite list where every element is `x`."""
    return LazyList(lambda *_: item, inf=True)


def iterate(f, x):
    """Returns an infinite list of repeated applications of `f` to `x`."""
    pass


def cycle(xs):
    """Returns an infinite list which is an infinite repetition of `xs`."""
    return LazyList(lambda _, i: xs[i % len(xs)], inf=True)


naturals = LazyList(lambda _, i: i, inf=True)
"""List of natural numbers."""
zeros = LazyList(lambda *_: 0, inf=True)
"""List of zeros."""
ones = LazyList(lambda *_: 1, inf=True)
"""List of ones."""
empty = LazyList(None, const(0))
"""Empty list."""
