
from Hittable import Hittable, HitRecord
from Interval import Interval
from Aabb import Aabb
from Ray import Ray
from Vec3 import Vec3

class BVHNode(Hittable):
    @staticmethod
    def box_compare(a, b, axis_index):
        a_axis = a.bounding_box().axis_interval(axis_index)
        b_axis = b.bounding_box().axis_interval(axis_index)
        return a_axis.min < b_axis.min

    @staticmethod
    def box_x_compare(a, b):
        return BVHNode.box_compare(a, b, 0)

    @staticmethod
    def box_y_compare(a, b):
        return BVHNode.box_compare(a, b, 1)

    @staticmethod
    def box_z_compare(a, b):
        return BVHNode.box_compare(a, b, 2)
    def __init__(self, objects, start=None, end=None):
        # Accepts either a HittableList or a list of Hittable objects
        if hasattr(objects, 'objects'):
            # If a HittableList is passed
            objects = objects.objects
        if start is None:
            start = 0
        if end is None:
            end = len(objects)
        object_span = end - start
        # Build the bounding box of the span of source objects
        bbox = None
        for object_index in range(start, end):
            obj_box = objects[object_index].bounding_box()
            if obj_box is not None:
                if bbox is None:
                    bbox = obj_box
                else:
                    bbox = Aabb(box0=bbox, box1=obj_box)
        if bbox is None:
            bbox = Aabb()  # empty
        axis = bbox.longest_axis()
        # Choose comparator based on axis
        if axis == 0:
            comparator = BVHNode.box_x_compare
        elif axis == 1:
            comparator = BVHNode.box_y_compare
        else:
            comparator = BVHNode.box_z_compare
        if object_span == 1:
            self.left = self.right = objects[start]
        elif object_span == 2:
            self.left = objects[start]
            self.right = objects[start + 1]
        else:
            sorted_objs = sorted(objects[start:end], key=lambda obj: obj.bounding_box().axis_interval(axis).min if obj.bounding_box() is not None else 0)
            mid = start + object_span // 2
            self.left = BVHNode(sorted_objs, 0, mid - start)
            self.right = BVHNode(sorted_objs, mid - start, object_span)
        box_left = self.left.bounding_box()
        box_right = self.right.bounding_box()
        if box_left is None or box_right is None:
            self.bbox = None
        else:
            self.bbox = Aabb(box0=box_left, box1=box_right)

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        if self.bbox is None or not self.bbox.hit(r, ray_t):
            return False
        hit_left = self.left.hit(r, ray_t, rec)
        hit_right = self.right.hit(r, Interval(ray_t.min, rec.t if hit_left else ray_t.max), rec)
        return hit_left or hit_right

    def bounding_box(self):
        return self.bbox
