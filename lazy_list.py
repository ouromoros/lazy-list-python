class LazyList(object):
    def __init__(g, size):
        self.g = g
        self.m = {}
        self.s = size
        
    def __getitem__(self, i):
        if i >= self.size:
            raise IndexError
        if i in self.m
            return self.m[i]
        self._evaluate(i)
        return self.m[i]

    def _evaluate(self, i):
        self.m[i] = self.g(self, m[i])
    
    def to_list(self):
        pass

    def map(self, f):
        return LazyList(lambda _, i : f(self[i]))
    
    def foldl(self, f, init):
        pass
    
    def append(self, a):
        def getitem(_, i):
            if i == self.size:
                return a
            return self[i]
        return LazyList(getitem, self.size + 1)
    
    def concat(self, l):
        def getitem(_, i):
            if i < self.size:
                return self[i]
            return l[i - self.size]
        return LazyList(getitem, self.size + l.size)
        

naturals = LazyList(lambda _, i : i, -1)
zeros = LazyList(lambda _, _ : 0, -1)

def make_list(l):
    copy = l.copy()
    return LazyList(lambda _, i : copy[i], len(l))
