from Ray import Ray
from Vec3 import Vec3, Color
from Texture import Texture, SolidColor
import math
import random

class Material:
    def scatter(self, ray_in, hit_record):
        # By default, materials do not scatter
        return False, None, None

    def emitted(self, u, v, p):
        # By default, materials do not emit light
        return Color(0, 0, 0)
    
class Lambertian(Material):
    def __init__(self, albedo_or_texture):
        # Accepts either a Color or a Texture
        if isinstance(albedo_or_texture, Texture):
            self.tex = albedo_or_texture
        else:
            self.tex = SolidColor(albedo_or_texture)

    def scatter(self, ray_in, hit_record):
        scatter_direction = hit_record.normal + Vec3.random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal
        scattered = Ray(hit_record.p, scatter_direction, ray_in.time())
        attenuation = self.tex.value(hit_record.u, hit_record.v, hit_record.p)
        return True, scattered, attenuation
        
class Metal(Material):
    def __init__(self, albedo, fuzz=0.0):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, ray_in, hit_record):
        reflected = Vec3.reflect(ray_in.direction(), hit_record.normal)
        direction = Vec3.unit_vector(reflected) + (self.fuzz * Vec3.random_unit_vector())
        scattered = Ray(hit_record.p, direction, ray_in.time())
        attenuation = self.albedo
        return (Vec3.dot(scattered.direction(), hit_record.normal) > 0), scattered, attenuation

class Dielectric(Material):
    def __init__(self, ir):  # Index of Refraction
        self.ir = ir

    def scatter(self, ray_in, hit_record):
        attenuation = Color(1.0, 1.0, 1.0)
        refraction_ratio = 1.0/self.ir if hit_record.front_face else self.ir

        unit_direction = Vec3.unit_vector(ray_in.direction())
        cos_theta = min(Vec3.dot(-unit_direction, hit_record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, refraction_ratio) > random.random():
            direction = Vec3.reflect(unit_direction, hit_record.normal)
        else:
            direction = Vec3.refract(unit_direction, hit_record.normal, refraction_ratio)

        scattered = Ray(hit_record.p, direction, ray_in.time())
        return True, scattered, attenuation


    def reflectance(self, cosine, ref_idx):
        # Use Schlick's approximation for reflectance.
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)


# DiffuseLight material for emissive surfaces
class DiffuseLight(Material):
    def __init__(self, tex_or_color):
        # Accepts either a Texture or a Color
        if isinstance(tex_or_color, Texture):
            self.tex = tex_or_color
        else:
            self.tex = SolidColor(tex_or_color)

    def emitted(self, u, v, p):
        return self.tex.value(u, v, p)
    
class DiffuseLight(Material):
    def __init__(self, tex_or_color):
        # Accepts either a Texture or a Color
        if isinstance(tex_or_color, Texture):
            self.tex = tex_or_color
        else:
            self.tex = SolidColor(tex_or_color)

    def emitted(self, u, v, p):
        return self.tex.value(u, v, p)

class Isotropic(Material):
    def __init__(self, tex_or_color):
        if isinstance(tex_or_color, Texture):
            self.tex = tex_or_color
        else:
            self.tex = SolidColor(tex_or_color)

    def scatter(self, ray_in, hit_record):
        scatter_direction = Vec3.random_unit_vector()
        scattered = Ray(hit_record.p, scatter_direction, ray_in.time())
        attenuation = self.tex.value(hit_record.u, hit_record.v, hit_record.p)
        return True, scattered, attenuation

