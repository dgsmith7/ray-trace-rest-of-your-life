from Ray import Ray
from Vec3 import Vec3, Color
from Texture import Texture, SolidColor
from Onb import Onb
import math
import random
from typing import Tuple, Optional
from Pdf import Pdf

class ScatterRecord:
    def __init__(self):
        self.attenuation = Color(1, 1, 1)
        self.pdf_ptr: Optional[Pdf] = None  # Should be an instance of Pdf
        self.skip_pdf = False
        self.skip_pdf_ray: Optional[Ray] = None  # Should be an instance of Ray

class Material:
    def scatter(self, ray_in, hit_record, srec: ScatterRecord) -> bool:
        # By default, materials do not scatter
        return False

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

    def scatter(self, ray_in, hit_record, srec: ScatterRecord) -> bool:
        from Pdf import CosinePdf
        srec.attenuation = self.tex.value(hit_record.u, hit_record.v, hit_record.p)
        srec.pdf_ptr = CosinePdf(hit_record.normal)
        srec.skip_pdf = False
        srec.skip_pdf_ray = None
        return True

    def scattering_pdf(self, ray_in, hit_record, scattered) -> float:
        cos_theta = Vec3.dot(hit_record.normal, Vec3.unit_vector(scattered.direction()))
        return 0.0 if cos_theta < 0 else cos_theta / math.pi

class Metal(Material):
    def __init__(self, albedo, fuzz=0.0):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, ray_in, hit_record, srec: ScatterRecord) -> bool:
        reflected = Vec3.reflect(ray_in.direction(), hit_record.normal)
        reflected = Vec3.unit_vector(reflected) + (self.fuzz * Vec3.random_unit_vector())
        srec.attenuation = self.albedo
        srec.pdf_ptr = None
        srec.skip_pdf = True
        srec.skip_pdf_ray = Ray(hit_record.p, reflected, ray_in.time())
        return True

class Dielectric(Material):
    def __init__(self, refraction_index):
        self.refraction_index = refraction_index

    def scatter(self, ray_in, hit_record, srec: ScatterRecord) -> bool:
        srec.attenuation = Color(1.0, 1.0, 1.0)
        srec.pdf_ptr = None
        srec.skip_pdf = True
        ri = 1.0 / self.refraction_index if hit_record.front_face else self.refraction_index
        unit_direction = Vec3.unit_vector(ray_in.direction())
        cos_theta = min(Vec3.dot(-unit_direction, hit_record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
        cannot_refract = ri * sin_theta > 1.0
        if cannot_refract or self.reflectance(cos_theta, ri) > random.random():
            direction = Vec3.reflect(unit_direction, hit_record.normal)
        else:
            direction = Vec3.refract(unit_direction, hit_record.normal, ri)
        srec.skip_pdf_ray = Ray(hit_record.p, direction, ray_in.time())
        return True

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

    def scatter(self, ray_in, hit_record, srec: ScatterRecord) -> bool:
        from Pdf import SpherePdf
        srec.attenuation = self.tex.value(hit_record.u, hit_record.v, hit_record.p)
        srec.pdf_ptr = SpherePdf()
        srec.skip_pdf = False
        srec.skip_pdf_ray = None
        return True

    def scattering_pdf(self, ray_in, hit_record, scattered) -> float:
        return 1.0 / (4.0 * math.pi)
    
class EmptyMaterial(Material):
    def scatter(self, ray_in, hit_record, srec):
        return False