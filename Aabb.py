from Interval import Interval
from Vec3 import Point3, Vec3
from Ray import Ray

class Aabb:

    def __add__(self, offset):
        # Allow Aabb + Vec3
        if not isinstance(offset, Vec3):
            return NotImplemented
        from Interval import Interval
        return Aabb(
            Interval(self.x.min + offset.x(), self.x.max + offset.x()),
            Interval(self.y.min + offset.y(), self.y.max + offset.y()),
            Interval(self.z.min + offset.z(), self.z.max + offset.z())
        )

    def __radd__(self, offset):
        # Allow Vec3 + Aabb
        return self.__add__(offset)
    
    def longest_axis(self):
        x_size = self.x.size()
        y_size = self.y.size()
        z_size = self.z.size()
        if x_size > y_size and x_size > z_size:
            return 0
        elif y_size > z_size:
            return 1
        else:
            return 2
        
    @staticmethod
    def surrounding_box(box0, box1):
        small = Point3(
            min(box0.x.min, box1.x.min),
            min(box0.y.min, box1.y.min),
            min(box0.z.min, box1.z.min)
        )
        big = Point3(
            max(box0.x.max, box1.x.max),
            max(box0.y.max, box1.y.max),
            max(box0.z.max, box1.z.max)
        )
        return Aabb(a=small, b=big)
    
    def __init__(self, x=None, y=None, z=None, a=None, b=None, box0=None, box1=None):
        if box0 is not None and box1 is not None:
            # Construct from two Aabb boxes
            self.x = Interval(a=box0.x, b=box1.x)
            self.y = Interval(a=box0.y, b=box1.y)
            self.z = Interval(a=box0.z, b=box1.z)
            self.pad_to_minimums()
        elif a is not None and b is not None:
            # Construct from two points
            self.x = Interval(min(a[0], b[0]), max(a[0], b[0]))
            self.y = Interval(min(a[1], b[1]), max(a[1], b[1]))
            self.z = Interval(min(a[2], b[2]), max(a[2], b[2]))
            self.pad_to_minimums()
        elif x is not None and y is not None and z is not None:
            # Construct from three intervals
            self.x = x
            self.y = y
            self.z = z
            self.pad_to_minimums()
        else:
            # Default: empty box
            self.x = Interval()
            self.y = Interval()
            self.z = Interval()
            self.pad_to_minimums()

    def pad_to_minimums(self):
        delta = 0.0001
        if self.x.size() < delta:
            self.x = self.x.expand(delta)
        if self.y.size() < delta:
            self.y = self.y.expand(delta)
        if self.z.size() < delta:
            self.z = self.z.expand(delta)


    def axis_interval(self, n):
        if n == 1:
            return self.y
        if n == 2:
            return self.z
        return self.x

    def hit(self, r: Ray, ray_t: Interval) -> bool:
        ray_orig = r.origin()
        ray_dir = r.direction()
        tmin = ray_t.min
        tmax = ray_t.max
        for axis in range(3):
            ax = self.axis_interval(axis)
            adinv = 1.0 / ray_dir[axis] if ray_dir[axis] != 0 else float('inf')
            t0 = (ax.min - ray_orig[axis]) * adinv
            t1 = (ax.max - ray_orig[axis]) * adinv
            if t0 < t1:
                tmin = max(t0, tmin)
                tmax = min(t1, tmax)
            else:
                tmin = max(t1, tmin)
                tmax = min(t0, tmax)
            if tmax <= tmin:
                return False
        return True

    def longest_axis(self):
        x_size = self.x.size()
        y_size = self.y.size()
        z_size = self.z.size()
        if x_size > y_size:
            return 0 if x_size > z_size else 2
        else:
            return 1 if y_size > z_size else 2

# Static empty and universe boxes
Aabb.empty = Aabb(x=Interval.empty, y=Interval.empty, z=Interval.empty)
Aabb.universe = Aabb(x=Interval.universe, y=Interval.universe, z=Interval.universe)
