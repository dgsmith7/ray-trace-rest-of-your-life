import math
import random

class Vec3:
    def unit(self):
        len = self.length()
        if len == 0:
            return Vec3(0, 0, 0)
        return self / len
    @staticmethod
    def random_int(min_val, max_val):
        # Returns a random integer in [min_val, max_val]
        return int(Vec3.random_double(min_val, max_val + 1))
    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.e = [e0, e1, e2]

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, i):
        return self.e[i]

    def __setitem__(self, i, value):
        self.e[i] = value

    def __iadd__(self, v):
    # Handle both Vec3 and numeric types
        if isinstance(v, Vec3):
            self.e[0] += v.e[0]
            self.e[1] += v.e[1]
            self.e[2] += v.e[2]
        elif isinstance(v, (int , float)):
            # Handle case where v is a number
            self.e[0] += v
            self.e[1] += v
            self.e[2] += v
        else:
            raise TypeError(f"Unsupported operand type for +=: '{type(self).__name__}' and '{type(v).__name__}'")
        return self

    def __imul__(self, t):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self

    def __itruediv__(self, t):
        return self.__imul__(1/t)

    def __add__(self, v):
        return Vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])

    def __sub__(self, v):
        return Vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])

    def __mul__(self, t):
        if isinstance(t, Vec3):
            return Vec3(self.e[0] * t.e[0], self.e[1] * t.e[1], self.e[2] * t.e[2])
        else:
            return Vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)

    def __rmul__(self, t):
        return self.__mul__(t)

    def __truediv__(self, t):
        return Vec3(self.e[0] / t, self.e[1] / t, self.e[2] / t)

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.e[0]**2 + self.e[1]**2 + self.e[2]**2

    def near_zero(self):
        s = 1e-8
        return (abs(self.e[0]) < s) and (abs(self.e[1]) < s) and (abs(self.e[2]) < s)

    def random_double(min, max):
        return min + (max - min) * random.random()
    
    @staticmethod
    def random():
        return Vec3(random.random(), random.random(), random.random())

    @staticmethod
    def random_range(min, max):
        return Vec3(Vec3.random_double(min, max), Vec3.random_double(min, max), Vec3.random_double(min, max))

# Vector Utility Functions

    def vec3_add(u, v):
        return Vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2])
    
    def vec3_sub(u, v):
        return Vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2])
    
    def vec3_mul(u, v):
        return Vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2])
    
    def vec3_mul_scalar(t, v):
        return Vec3(t * v.e[0], t * v.e[1], t * v.e[2])
    
    def vec3_div_scalar(v, t):
        if (t == 0):
            t = 1e-8
        return Vec3(v.e[0] / t, v.e[1] / t, v.e[2] / t)
    
    def dot(u, v):
        return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

    def cross(u, v):
        return Vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
                    u.e[2] * v.e[0] - u.e[0] * v.e[2],
                    u.e[0] * v.e[1] - u.e[1] * v.e[0])
    
    def unit_vector(v):
        #return Vec3.vec3_div_scalar(v, v.length())
        length = v.length()
        if length == 0:
            return Vec3(0, 0, 0)
        return v / length
    
    def random_unit_vector():
        while True:
            p = Vec3.random_range(-1, 1)
            lensq = p.length_squared()
            if 1e-160 < lensq <= 1.0:
                return Vec3.vec3_div_scalar(p, math.sqrt(lensq))

    def random_in_unit_disk():
        while True:
            p = Vec3(Vec3.random_double(-1, 1), Vec3.random_double(-1, 1), 0)
            if p.length_squared() < 1:
                return p

    def random_on_hemisphere(normal):
        on_unit_sphere = Vec3.random_unit_vector()
        if Vec3.dot(on_unit_sphere, normal) > 0.0:
            return on_unit_sphere
        else:
            return -on_unit_sphere

    def reflect(v, n):
        #return Vec3.vec3_sub(v, Vec3.vec3_mul_scalar(2 * Vec3.dot(v, n), n))
        return v - 2*Vec3.dot(v,n)*n
        #return v - n * ((v[0] * n[0] + v[1] * n[1] + v[2] * n[2] ) * 2)
    
    # def refract(uv, n, etai_over_etat):
    #     cos_theta = min(Vec3.dot(-uv, n), 1.0)
    #     r_out_perp = etai_over_etat * (uv + cos_theta * n)
    #     r_out_parallel = math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n # this could be part of it +/-
    #     #r_out_perp = Vec3.vec3_mul_scalar(etai_over_etat, Vec3.vec3_add(uv, Vec3.vec3_mul_scalar(cos_theta, n)))
    #     #r_out_parallel = Vec3.vec3_mul_scalar(-math.sqrt(abs(1.0 - r_out_perp.length_squared())), n)
    #     return r_out_perp + r_out_parallel

    # @staticmethod
    def refract(uv, n, etai_over_etat):
        cos_theta = min(Vec3.dot(-uv, n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta * n)
        r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel

# Point3 is just an alias for Vec3, but useful for geometric clarity in the code.
Point3 = Vec3

# Color is just an alias for Vec3, but useful for clarity in the code.
Color = Vec3


