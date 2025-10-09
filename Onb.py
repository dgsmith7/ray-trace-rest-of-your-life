import math
from Vec3 import Vec3

class Onb:
    def __init__(self, n: Vec3):
        self.axis = [Vec3(0,0,0), Vec3(0,0,0), Vec3(0,0,0)]
        self.axis[2] = Vec3.unit_vector(n)
        # Choose a vector not parallel to axis[2]
        if abs(self.axis[2].x()) > 0.9:
            a = Vec3(0, 1, 0)
        else:
            a = Vec3(1, 0, 0)
        self.axis[1] = Vec3.unit_vector(Vec3.cross(self.axis[2], a))
        self.axis[0] = Vec3.cross(self.axis[2], self.axis[1])

    def u(self) -> Vec3:
        return self.axis[0]

    def v(self) -> Vec3:
        return self.axis[1]

    def w(self) -> Vec3:
        return self.axis[2]

    def transform(self, v: Vec3) -> Vec3:
        # Transform from basis coordinates to local space.
        return (v.x() * self.u()) + (v.y() * self.v()) + (v.z() * self.w())