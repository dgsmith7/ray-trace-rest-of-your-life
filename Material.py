from Ray import Ray
from Vec3 import Vec3, Color
from Texture import Texture, SolidColor
from Onb import Onb
import math
import random
from typing import Tuple

class Material:
    def scatter(self, ray_in, hit_record) -> Tuple[bool, Ray, Color, float]:
        # By default, materials do not scatter
        return False, Ray(hit_record.p, Vec3(0,0,0), 0), Color(1,1,1), 1.0

    def emitted(self, ray_in, hit_record, u, v, p):
        # By default, materials do not emit light
        return Color(0, 0, 0)
    
    def scattering_pdf(self, ray_in, hit_record, scattered) -> float:
        # By default, materials do not have a scattering PDF
        return 0.0

class Lambertian(Material):
    def __init__(self, albedo_or_texture):
        if isinstance(albedo_or_texture, Texture):
            self.tex = albedo_or_texture
        else:
            self.tex = SolidColor(albedo_or_texture)

    def scatter(self, ray_in, hit_record) -> Tuple[bool, Ray, Color, float]:
        uvw = Onb(hit_record.normal)
        scatter_direction = uvw.transform(Vec3.random_cosine_direction())
        scattered = Ray(hit_record.p, Vec3.unit_vector(scatter_direction), ray_in.time())
        attenuation = self.tex.value(hit_record.u, hit_record.v, hit_record.p)
        pdf = Vec3.dot(uvw.w(), scattered.direction()) / math.pi
        return True, scattered, attenuation, pdf

    def scattering_pdf(self, ray_in, hit_record, scattered) -> float:
        cosine = Vec3.dot(hit_record.normal, Vec3.unit_vector(scattered.direction()))
        return cosine / math.pi if cosine > 0 else 0.0

class Metal(Material):
    def __init__(self, albedo, fuzz=0.0):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, ray_in, hit_record) -> Tuple[bool, Ray, Color, float]:
        reflected = Vec3.reflect(ray_in.direction(), hit_record.normal)
        direction = Vec3.unit_vector(reflected) + (self.fuzz * Vec3.random_unit_vector())
        scattered = Ray(hit_record.p, direction, ray_in.time())
        attenuation = self.albedo
        pdf = 1.0
        return (Vec3.dot(scattered.direction(), hit_record.normal) > 0), scattered, attenuation, pdf

class Dielectric(Material):
    def __init__(self, ir):
        self.ir = ir

    def scatter(self, ray_in, hit_record) -> Tuple[bool, Ray, Color, float]:
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
        pdf = 1.0
        return True, scattered, attenuation, pdf

    def reflectance(self, cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)

class DiffuseLight(Material):
    def __init__(self, tex_or_color):
        if isinstance(tex_or_color, Texture):
            self.tex = tex_or_color
        else:
            self.tex = SolidColor(tex_or_color)

    def emitted(self, ray_in, hit_record, u, v, p):
        if not getattr(hit_record, "front_face", True):
            return Color(0, 0, 0)
        return self.tex.value(u, v, p)

class Isotropic(Material):
    def __init__(self, tex_or_color):
        if isinstance(tex_or_color, Texture):
            self.tex = tex_or_color
        else:
            self.tex = SolidColor(tex_or_color)

    def scatter(self, ray_in, hit_record) -> Tuple[bool, Ray, Color, float]:
        scatter_direction = Vec3.random_unit_vector()
        scattered = Ray(hit_record.p, scatter_direction, ray_in.time())
        attenuation = self.tex.value(hit_record.u, hit_record.v, hit_record.p)
        pdf = 1.0 / (4.0 * math.pi)
        return True, scattered, attenuation, pdf

    def scattering_pdf(self, ray_in, hit_record, scattered) -> float:
        return 1.0 / (4.0 * math.pi)