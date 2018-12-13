import functools


def finite(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self.inf:
            raise ValueError("Invalid Operation on Infinite List!")
        return func(self, *args, **kwargs)
    return wrap


class LazyList(object):

    def __init__(self, generator, size=None, inf=False):
        self.g = generator
        self.m = dict()
        self.size = size
        self.inf = inf

    def __len__(self):
        if self.inf:
            raise ValueError
        if self.size:
            return self.size
        i = max(self.m.keys(), default=0)
        while True:
            try:
                self[i]
            except IndexError:
                break
            i += 1
        self.size = i
        return self.size

    def __contains(self, item):
        return self.elem_index(item) != -1

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.start or 0, key.stop or self.size, key.step or 1
            if stop:
                size = (stop - start) // step + 1
                return LazyList(lambda _, i: self[start + i * step], size)
            return LazyList(lambda _, i: self[start + i * step], inf=True)
        elif isinstance(key, int):
            if key in self.m:
                return self.m[key]
            self._evaluate(key)
            return self.m[key]
        else:
            raise IndexError("Index can only be slice or integer!")

    def _evaluate(self, i):
        self.m[i] = self.g(self, i)

    def map(self, f):
        return LazyList(lambda _, i: f(self[i]), self.size)

    @finite
    def to_list(self):
        return [self[i] for i in range(len(self))]

    @finite
    def append(self, a):
        def getitem(_, i):
            if i == self.size:
                return a
            return self[i]
        return LazyList(getitem, self.size + 1)

    @finite
    def concat(self, l):
        def getitem(_, i):
            if i < self.size:
                return self[i]
            return l[i - self.size]

        if l.inf:
            inf = True
        else:
            inf = False
        if self.size and l.size:
            size = self.size + l.size
        else:
            size = None
        return LazyList(getitem, size, inf)

    @finite
    def reverse(self):
        return LazyList(lambda _, i: self[self.size - 1 - i], self.size)

    def filter(self, f):
        data = []
        last_index = 0

        def getitem(_, i):
            nonlocal last_index
            if i >= len(data):
                for _ in range(len(data), i + 1):
                    while not f(self[last_index]):
                        last_index += 1
                    data.append(self[last_index])
                    last_index += 1
            return data[i]
        return LazyList(getitem, inf=self.inf)

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
        return LazyList(lambda _, i: self[i + 1])

    def take(self, n):
        return LazyList(lambda _, i: self[i], n)

    def takeWhile(self, f, n):
        return self.filter(f).take(n)

    def drop(self, n):
        pass

    def flat_map(self, f):
        pass

    def replicate(self, n):
        pass

    def zip(self, *args):
        pass


naturals = LazyList(lambda _, i: i, inf=True)
zeros = LazyList(lambda _, i: 0, inf=True)
ones = LazyList(lambda _, i: 1, inf=True)
empty = LazyList(None, 0)


def make_lazy_list(iterable):
    copy = list(iterable)
    return LazyList(lambda _, i: copy[i], len(copy))


def repeat(item):
    return LazyList(lambda _, i: item, inf=True)
