import math
from abc import ABC, abstractmethod
from Vec3 import Point3, Vec3
from Ray import Ray
from Interval import Interval
from Material import Material

class HitRecord:
    def __init__(self):
        self.p = Point3()         # Hit point
        self.normal = Vec3()      # Surface normal at hit
        self.mat = None           # Material at hit
        self.t = 0.0              # Ray parameter at hit
        self.u = 0.0              # U texture coordinate
        self.v = 0.0              # V texture coordinate
        self.front_face = False   # Whether the hit was on the outside

    def set_face_normal(self, r, outward_normal):
        """
        Sets the hit record normal vector and determines if the hit was on the outside (front face).
        The parameter `outward_normal` is assumed to have unit length.
        """
        self.front_face = Vec3.dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        pass

    @abstractmethod
    def bounding_box(self):
        pass

# Translate wrapper for hittable objects
class Translate(Hittable):
    def __init__(self, obj, offset):
        self.object = obj  # Hittable
        self.offset = offset  # Vec3
        bbox = self.object.bounding_box()
        if bbox is not None:
            self.bbox = bbox + self.offset
        else:
            self.bbox = None

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        # Move the ray backwards by the offset
        offset_r = Ray(r.origin() - self.offset, r.direction(), r.time())
        # Determine whether an intersection exists along the offset ray (and if so, where)
        if not self.object.hit(offset_r, ray_t, rec):
            return False
        # Move the intersection point forwards by the offset
        rec.p += self.offset
        return True

    def bounding_box(self):
        return self.bbox
    
class RotateY(Hittable):
    def __init__(self, obj, angle_degrees):
        self.object = obj  # Hittable
        radians = math.radians(angle_degrees)
        self.sin_theta = math.sin(radians)
        self.cos_theta = math.cos(radians)
        bbox = obj.bounding_box()
        if bbox is not None:
            min_pt = Point3(float('inf'), float('inf'), float('inf'))
            max_pt = Point3(-float('inf'), -float('inf'), -float('inf'))
            # Loop over all 8 corners of the bounding box
            for i in [0, 1]:
                for j in [0, 1]:
                    for k in [0, 1]:
                        x = i * bbox.x.max + (1 - i) * bbox.x.min
                        y = j * bbox.y.max + (1 - j) * bbox.y.min
                        z = k * bbox.z.max + (1 - k) * bbox.z.min
                        newx = self.cos_theta * x + self.sin_theta * z
                        newz = -self.sin_theta * x + self.cos_theta * z
                        tester = [newx, y, newz]
                        for c in range(3):
                            min_pt[c] = min(min_pt[c], tester[c])
                            max_pt[c] = max(max_pt[c], tester[c])
            from Aabb import Aabb
            self.bbox = Aabb(a=min_pt, b=max_pt)
        else:
            self.bbox = None

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        # Transform the ray from world space to object space
        origin = Point3(
            self.cos_theta * r.origin().x() - self.sin_theta * r.origin().z(),
            r.origin().y(),
            self.sin_theta * r.origin().x() + self.cos_theta * r.origin().z()
        )
        direction = Vec3(
            self.cos_theta * r.direction().x() - self.sin_theta * r.direction().z(),
            r.direction().y(),
            self.sin_theta * r.direction().x() + self.cos_theta * r.direction().z()
        )
        rotated_r = Ray(origin, direction, r.time())
        # Determine whether an intersection exists in object space (and if so, where)
        if not self.object.hit(rotated_r, ray_t, rec):
            return False
        # Transform the intersection from object space back to world space
        p = rec.p
        rec.p = Point3(
            self.cos_theta * p.x() + self.sin_theta * p.z(),
            p.y(),
            -self.sin_theta * p.x() + self.cos_theta * p.z()
        )
        n = rec.normal
        rec.normal = Vec3(
            self.cos_theta * n.x() + self.sin_theta * n.z(),
            n.y(),
            -self.sin_theta * n.x() + self.cos_theta * n.z()
        )
        return True

    def bounding_box(self):
        return self.bbox
