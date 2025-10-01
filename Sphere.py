import math
from Hittable import Hittable, HitRecord
from Vec3 import Point3, Vec3
from Ray import Ray
from Interval import Interval

from Material import Material#
from Aabb import Aabb


class Sphere(Hittable):
    @staticmethod
    def get_sphere_uv(p):
        # p: a point on the unit sphere, returns (u, v) in [0,1]x[0,1]
        theta = math.acos(-p.y())
        phi = math.atan2(-p.z(), p.x()) + math.pi
        u = phi / (2 * math.pi)
        v = theta / math.pi
        return u, v
    
    def __init__(self, center1: Point3, radius: float, mat: Material, center2: Point3 = None):
        # If center2 is None, stationary sphere. Otherwise, moving sphere.
        self.center1 = center1
        if center2 is not None:
            self.center_vec = center2 - center1
        else:
            self.center_vec = Vec3(0, 0, 0)
        self.radius = max(0, radius)
        self.mat = mat
        rvec = Vec3(self.radius, self.radius, self.radius)
        if center2 is None:
            # Stationary sphere
            self.bbox = Aabb(a=self.center1 - rvec, b=self.center1 + rvec)
        else:
            # Moving sphere: bbox is the surrounding box of the sphere at t=0 and t=1
            box1 = Aabb(a=self.center(0.0) - rvec, b=self.center(0.0) + rvec)
            box2 = Aabb(a=self.center(1.0) - rvec, b=self.center(1.0) + rvec)
            self.bbox = Aabb.surrounding_box(box1, box2)

    def bounding_box(self):
        return self.bbox

    def center(self, time: float) -> Point3:
        return self.center1 + time * self.center_vec

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        sphere_center = self.center(r.time())
        oc = sphere_center - r.origin()
        a = r.direction().length_squared()
        h = Vec3.dot(r.direction(), oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c
        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        if (a == 0):
            a = 1e-8
        root = (h - sqrtd) / a
        if not (ray_t.surrounds(root)):
            root = (h + sqrtd) / a
            if not (ray_t.surrounds(root)):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - sphere_center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.u, rec.v = self.get_sphere_uv(outward_normal)
        rec.mat = self.mat

        return True