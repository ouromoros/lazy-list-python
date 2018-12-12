import functools

class LazyList(object):
    def finite(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if self.size == -1:
                raise ValueError("Invalid Operation on Infinite List!")
            func(self, *args, **kwargs)
        return wrap

    def __init__(self, generator, size):
        self.size = size
        self.g = generator
        self.m = {}

    def __len__(self):
        return self.size

    def __getitem__(self, s):
        if isinstance(s, slice):
            start, stop, step = s.start or 0, s.stop or self.size, s.step or 1
            if self.size == -1:
                size = -1
            else:
                size = (step - start) // stop + 1
            return LazyList(lambda _, i : self[start + i * step], size)
        elif isinstance(s, int):
            if  != -1 and i >= self.size:
                raise IndexError
            if i in self.m
                return self.m[i]
            self._evaluate(i)
            return self.m[i]
        else:
            raise IndexError
        
    def _evaluate(self, i):
        self.m[i] = self.g(self, m[i])
    
    def map(self, f):
        return LazyList(lambda _, i : f(self[i]))

    @finite
    def to_list(self):
        return list(self[i] for i in range(self.size))

    @finite
    def foldl(self, f, init):
        r = init
        for i in range(self.size):
            r = f(r, self[i])
        return r
    
    @finite
    def foldr(self, f, init):
        pass
    
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
        if l.size == -1:
            size = -1
        else:
            size = self.size + l.size
        return LazyList(getitem, size)

    @finite
    def reverse(self):
        pass
    
    def filter(self, f):
        pass
    
    def partition(self, f):
        pass
    
    def elemIndex(self, v):
        pass
    
    def tails(self):
        pass
    
    def take(self, n):
        pass
    
    def takeWhile(self, f):
        pass
    
    def drop(self, n):
        pass
    
    def flat_map(self):
        pass
    
    def replicate(self, n):
        pass
    
    def zip(self, *args):
        pass

naturals = LazyList(lambda _, i : i, -1)
zeros = LazyList(lambda _, _ : 0, -1)
ones = LazyList(lambda _, _ : 1, -1)
empty = LazyList(_, 0)

def make_list(l):
    copy = l.copy()
    return LazyList(lambda _, i : copy[i], len(l))

def repeat(v):
    pass
