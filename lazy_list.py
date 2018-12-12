import functools

def finite(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if self.size == -1:
            raise ValueError("Invalid Operation on Infinite List!")
        func(self, *args, **kwargs)
    return wrap

class LazyList(object):

    def __init__(self, generator, size, is_inf = False):
        self.g = generator
        self.size = size
        self.is_inf = is_inf
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
            if self.size != -1 and s >= self.size:
                raise IndexError
            if s in self.m:
                return self.m[s]
            self._evaluate(s)
            return self.m[s]
        else:
            raise IndexError
        
    def _evaluate(self, i):
        self.m[i] = self.g(self, self.m[i])
    
    def map(self, f):
        return LazyList(lambda _, i : f(self[i]), self.size)

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
        return LazyList(lambda _, i : self[self.size - 1 - i], self.size)
    
    def filter(self, f):
        data = []
        last_index = 0
        def getitem(s, i):
            if i >= len(data):
                for j in range(len(data), i + 1):
                    while not f(self[last_index]):
                        last_index += 1
                    data.append(self[last_index])
            return data[i]
        return LazyList(getitem, -1)
    

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
