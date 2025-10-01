
import random
import math
import numpy as np

class Perlin:

    def turb(self, p, depth=7):
        accum = 0.0
        temp_p = p
        weight = 1.0
        for _ in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p = temp_p * 2
        return abs(accum)
    point_count = 256

    def __init__(self):
        from Vec3 import Vec3
        self.randvec = [Vec3.random_unit_vector() for _ in range(self.point_count)]
        self.perm_x = self.perlin_generate_perm()
        self.perm_y = self.perlin_generate_perm()
        self.perm_z = self.perlin_generate_perm()

    def noise(self, p):
        # p is expected to be a Vec3 or similar with x(), y(), z() methods
        u = p.x() - math.floor(p.x())
        v = p.y() - math.floor(p.y())
        w = p.z() - math.floor(p.z())
        # Hermite cubic smoothing
        u = u * u * (3 - 2 * u)
        v = v * v * (3 - 2 * v)
        w = w * w * (3 - 2 * w)
        i = int(math.floor(p.x()))
        j = int(math.floor(p.y()))
        k = int(math.floor(p.z()))
        c = [[[None for _ in range(2)] for _ in range(2)] for _ in range(2)]
        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    idx = self.perm_x[(i+di) & 255] ^ self.perm_y[(j+dj) & 255] ^ self.perm_z[(k+dk) & 255]
                    c[di][dj][dk] = self.randvec[idx]
        return self.perlin_interp(c, u, v, w, p)

    @staticmethod
    def perlin_interp(c, u, v, w, p):
        # c is a 2x2x2 array of Vec3, p is the original point
        from Vec3 import Vec3
        uu = u * u * (3 - 2 * u)
        vv = v * v * (3 - 2 * v)
        ww = w * w * (3 - 2 * w)
        accum = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = Vec3(u - i, v - j, w - k)
                    dot = Vec3.dot(c[i][j][k], weight_v)
                    accum += (i * uu + (1 - i) * (1 - uu)) \
                             * (j * vv + (1 - j) * (1 - vv)) \
                             * (k * ww + (1 - k) * (1 - ww)) \
                             * dot
        return accum

    @staticmethod
    def trilinear_interp(c, u, v, w):
        accum = 0.0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    accum += (i*u + (1-i)*(1-u)) \
                             * (j*v + (1-j)*(1-v)) \
                             * (k*w + (1-k)*(1-w)) \
                             * c[i][j][k]
        return accum

    @classmethod
    def perlin_generate_perm(cls):
        p = list(range(cls.point_count))
        cls.permute(p)
        return p

    @staticmethod
    def permute(p):
        n = len(p)
        for i in range(n-1, 0, -1):
            target = random.randint(0, i)
            p[i], p[target] = p[target], p[i]
