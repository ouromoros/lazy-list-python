import functools


def check_finite(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self.inf:
            raise ValueError("Invalid Operation on Infinite List!")
        return func(self, *args, **kwargs)
    return wrap


def const(a):
    return lambda: a


class LazyList(object):

    def __init__(self, func, getsize=None, inf=False):
        self.func = func
        self.cache = dict()
        self.getsize = getsize
        self.inf = inf
        self.size = None

    def __len__(self):
        if self.inf:
            raise ValueError
        if self.size:
            return self.size
        if self.getsize:
            self.size = self.getsize()
            return self.size
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
            start, stop, step = key.start or 0, key.stop or self.size, key.step or 1
            if stop:
                size = (stop - start) // step + 1
                return LazyList(lambda _, i: self[start + i * step], const(size))
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

    def map(self, f):
        return LazyList(lambda _, i: f(self[i]), lambda: len(self), self.inf)

    @check_finite
    def to_list(self):
        return [self[i] for i in range(len(self))]

    @check_finite
    def append(self, a):
        def getitem(_, i):
            if i == len(self):
                return a
            return self[i]
        return LazyList(getitem, lambda: len(self) + 1)

    @check_finite
    def concat(self, l):
        def getitem(_, i):
            try:
                return self[i]
            except IndexError:
                return l[i - len(self)]

        if l.inf:
            inf = True
        else:
            inf = False
        return LazyList(getitem, lambda: len(self) + len(l), inf)

    @check_finite
    def reverse(self):
        return LazyList(lambda _, i: self[len(self) - 1 - i], lambda: len(self))

    def filter(self, f):
        data = []
        last_index = 0

        def getitem(_, i):
            nonlocal data
            nonlocal last_index
            if i >= len(data):
                for _ in range(len(data), i + 1):
                    while not f(self[last_index]):
                        last_index += 1
                    data.append(self[last_index])
                    last_index += 1
            return data[i]

        def getsize():
            nonlocal data
            nonlocal last_index
            while True:
                try:
                    while not f(self[last_index]):
                        last_index += 1
                    data.append(self[last_index])
                except IndexError:
                    break
                last_index += 1
            return len(data)
        return LazyList(getitem, getsize, self.inf)

    def partition(self, f):
        return (self.filter(f), self.filter(lambda x: not f(x)))

    def elem_index(self, item):
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

    def tails(self):
        return LazyList(lambda _, i: self[i + 1], lambda: len(self) - 1)

    def take(self, n):
        return LazyList(lambda _, i: self[i], const(n))

    def takeWhile(self, f, n):
        return self.filter(f).take(n)

    def drop(self, n):
        if self.size:
            size = self.size - n
        else:
            size = None
        return LazyList(lambda _, i: self[i + n], const(size), self.inf)

    def flat_map(self, f):
        pass

    def replicate(self, n):
        pass

    def zip(self, *args):
        pass
        # ls = args + [self]
        # return LazyList(lambda i: tuple(l[i] for l in ls))


naturals = LazyList(lambda _, i: i, inf=True)
zeros = LazyList(lambda *_: 0, inf=True)
ones = LazyList(lambda *_: 1, inf=True)
empty = LazyList(None, const(0))


def make_lazy_list(iterable):
    copy = list(iterable)
    return LazyList(lambda _, i: copy[i], const(len(copy)))


def repeat(item):
    return LazyList(lambda *_: item, inf=True)
