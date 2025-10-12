from Vec3 import Vec3
from Hittable import Hittable, HitRecord
from Ray import Ray
from Interval import Interval
from Aabb import Aabb

class HittableList(Hittable):
    def __init__(self, object=None):
        self.objects = []
        self.bbox = None
        if object:
            self.add(object)

    def clear(self):
        self.objects = []
        self.bbox = None

    def add(self, object):
        self.objects.append(object)
        obj_box = object.bounding_box()
        if obj_box is not None:
            if self.bbox is None:
                self.bbox = obj_box
            else:
                self.bbox = Aabb(box0=self.bbox, box1=obj_box)
    def bounding_box(self):
        return self.bbox

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = ray_t.max
        for obj in self.objects:
            if obj.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face
                rec.mat = temp_rec.mat
                rec.u = temp_rec.u
                rec.v = temp_rec.v
        return hit_anything
    
    def pdf_value(self, origin, direction):
        if not self.objects:
            return 0.0
        weight = 1.0 / len(self.objects)
        total = 0.0
        for obj in self.objects:
            total += weight * obj.pdf_value(origin, direction)
        return total

    def random(self, origin):
        if not self.objects:
            return Vec3(1, 0, 0)
        import random
        idx = random.randint(0, len(self.objects) - 1)
        return self.objects[idx].random(origin)