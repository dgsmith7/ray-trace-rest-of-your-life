import math
import random
from Hittable import Hittable, HitRecord
from Interval import Interval
from Vec3 import Vec3, Point3
from Ray import Ray
from Material import Material, Isotropic
from Aabb import Aabb
from Texture import Texture, SolidColor

class ConstantMedium(Hittable):
    def __init__(self, boundary, density, tex_or_color):
        self.boundary = boundary
        self.neg_inv_density = -1.0 / density
        self.phase_function = Isotropic(tex_or_color)

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        rec1 = HitRecord()
        rec2 = HitRecord()
        # Use an infinite interval for the boundary hits
        if not self.boundary.hit(r, Interval.universe, rec1):
            return False
        if not self.boundary.hit(r, Interval(rec1.t + 0.0001, float('inf')), rec2):
            return False
        if rec1.t < ray_t.min:
            rec1.t = ray_t.min
        if rec2.t > ray_t.max:
            rec2.t = ray_t.max
        if rec1.t >= rec2.t:
            return False
        if rec1.t < 0:
            rec1.t = 0
        ray_length = r.direction().length()
        distance_inside_boundary = (rec2.t - rec1.t) * ray_length
        hit_distance = self.neg_inv_density * math.log(random.random())
        if hit_distance > distance_inside_boundary:
            return False
        rec.t = rec1.t + hit_distance / ray_length
        rec.p = r.at(rec.t)
        rec.normal = Vec3(1, 0, 0)  # arbitrary
        rec.front_face = True       # also arbitrary
        rec.mat = self.phase_function
        return True

    def bounding_box(self):
        return self.boundary.bounding_box()
