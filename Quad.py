# Helper function to create a box from two points and a material
from HittableList import HittableList
def box(a, b, mat):
    # Returns a HittableList of six quads forming a box from two opposite corners
    min_pt = type(a)(min(a.x(), b.x()), min(a.y(), b.y()), min(a.z(), b.z()))
    max_pt = type(a)(max(a.x(), b.x()), max(a.y(), b.y()), max(a.z(), b.z()))
    dx = type(a)(max_pt.x() - min_pt.x(), 0, 0)
    dy = type(a)(0, max_pt.y() - min_pt.y(), 0)
    dz = type(a)(0, 0, max_pt.z() - min_pt.z())
    sides = HittableList()
    # front
    sides.add(Quad(type(a)(min_pt.x(), min_pt.y(), max_pt.z()), dx, dy, mat))
    # right
    sides.add(Quad(type(a)(max_pt.x(), min_pt.y(), max_pt.z()), -dz, dy, mat))
    # back
    sides.add(Quad(type(a)(max_pt.x(), min_pt.y(), min_pt.z()), -dx, dy, mat))
    # left
    sides.add(Quad(type(a)(min_pt.x(), min_pt.y(), min_pt.z()), dz, dy, mat))
    # top
    sides.add(Quad(type(a)(min_pt.x(), max_pt.y(), max_pt.z()), dx, -dz, mat))
    # bottom
    sides.add(Quad(type(a)(min_pt.x(), min_pt.y(), min_pt.z()), dx, dz, mat))
    return sides
from Hittable import Hittable
from Vec3 import Vec3
from Material import Material
from Aabb import Aabb
from Interval import Interval

class Quad(Hittable):
    def __init__(self, Q, u, v, mat):
        self.Q = Q              # Vec3: corner point
        self.u = u              # Vec3: edge vector
        self.v = v              # Vec3: edge vector
        self.mat = mat          # Material
        # Compute normal, D, and w as in C++ pseudocode
        n = self.u.cross(self.v)
        self.normal = n.unit()
        self.D = self.normal.dot(self.Q)
        self.w = n / n.dot(n)   # Vec3: w = n / dot(n, n)
        self.set_bounding_box()

    def set_bounding_box(self):
        # Compute the bounding box of all four vertices
        bbox_diagonal1 = Aabb(self.Q, self.Q + self.u + self.v)
        bbox_diagonal2 = Aabb(self.Q + self.u, self.Q + self.v)
        self.bbox = Aabb(bbox_diagonal1, bbox_diagonal2)

    def bounding_box(self):
        return self.bbox

    # ...existing code...

    # Additional attributes for C++ parity:
    # self.normal: Vec3, unit normal to the quad
    # self.D: float, plane constant

    def hit(self, r, ray_t, rec):
        # Ray-plane intersection
        denom = self.normal.dot(r.direction())
        if abs(denom) < 1e-8:
            return False  # Ray is parallel to the plane
        t = (self.D - self.normal.dot(r.origin())) / denom
        if not ray_t.contains(t):
            return False
        intersection = r.at(t)
        planar_hitpt_vector = intersection - self.Q
        alpha = self.w.dot(planar_hitpt_vector.cross(self.v))
        beta = self.w.dot(self.u.cross(planar_hitpt_vector))
        if not self.is_interior(alpha, beta, rec):
            return False
        rec.t = t
        rec.p = intersection
        rec.mat = self.mat
        rec.set_face_normal(r, self.normal)
        return True

    def is_interior(self, a, b, rec):
        # Check if (a, b) are within [0, 1] and set UVs
        unit_interval = Interval(0, 1)
        if not unit_interval.contains(a) or not unit_interval.contains(b):
            return False
        rec.u = a
        rec.v = b
        return True
