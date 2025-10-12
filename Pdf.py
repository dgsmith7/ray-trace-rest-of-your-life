from Vec3 import Vec3, Point3
import math
from Onb import Onb
import random

class Pdf:
    def value(self, direction: Vec3) -> float:
        raise NotImplementedError("Pdf.value() must be implemented by subclasses.")

    def generate(self) -> Vec3:
        raise NotImplementedError("Pdf.generate() must be implemented by subclasses.")

class SpherePdf(Pdf):
    def __init__(self):
        pass

    def value(self, direction: Vec3) -> float:
        return 1.0 / (4.0 * math.pi)

    def generate(self) -> Vec3:
        return Vec3.random_unit_vector()

class CosinePdf(Pdf):
    def __init__(self, w: Vec3):
        self.uvw = Onb(w)

    def value(self, direction: Vec3) -> float:
        cosine_theta = Vec3.dot(Vec3.unit_vector(direction), self.uvw.w())
        return max(0.0, cosine_theta / math.pi)

    def generate(self) -> Vec3:
        return self.uvw.transform(Vec3.random_cosine_direction())

class HittablePdf(Pdf):
    def __init__(self, objects, origin: Point3):
        # Import Hittable here to avoid circular import
        # from Hittable import Hittable
        self.objects = objects
        self.origin = origin

    def value(self, direction: Vec3) -> float:
        return self.objects.pdf_value(self.origin, direction)

    def generate(self) -> Vec3:
        return self.objects.random(self.origin)

class MixturePdf(Pdf):
    def __init__(self, p0: Pdf, p1: Pdf):
        self.p = [p0, p1]

    def value(self, direction: Vec3) -> float:
        return 0.5 * self.p[0].value(direction) + 0.5 * self.p[1].value(direction)

    def generate(self) -> Vec3:
        if random.random() < 0.5:
            return self.p[0].generate()
        else:
            return self.p[1].generate()