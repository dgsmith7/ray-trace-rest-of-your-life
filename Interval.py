from typing import ClassVar

class Interval:
    empty: ClassVar["Interval"]
    universe: ClassVar["Interval"]

    def __add__(self, displacement):
        if not isinstance(displacement, (int, float)):
            return NotImplemented
        return Interval(self.min + displacement, self.max + displacement)

    def __radd__(self, displacement):
        return self.__add__(displacement)
    
    def expand(self, delta):
        return Interval(self.min - delta, self.max + delta)
    
    def __init__(self, min_val=float('inf'), max_val=-float('inf'), a=None, b=None):
        if a is not None and b is not None:
            self.min = min(a.min, b.min)
            self.max = max(a.max, b.max)
        else:
            self.min = min_val
            self.max = max_val

    def size(self):
        return self.max - self.min

    def contains(self, x):
        return self.min <= x and x <= self.max

    def surrounds(self, x):
        return self.min < x and x < self.max
    
    def clamp(self, x):
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        else:
            return x

# Assign after class definition
Interval.empty = Interval(float('inf'), -float('inf'))
Interval.universe = Interval(-float('inf'), float('inf'))