from Hittable import HitRecord
from Vec3 import Color, Vec3, Point3
from Interval import Interval
from Ray import Ray
from color import write_color
from Pdf import CosinePdf
import math
import random
import datetime

class Camera:
    def __init__(self):
        self.aspect_ratio = 16.0 / 9.0
        self.image_width = 1200
        self.samples_per_pixel = 10
        self.max_depth = 10
        self.vfov = 20
        self.lookfrom = Point3(72, 40, 72)
        self.lookat = Point3(0, 0, 0)
        self.vup = Vec3(0, 1, 0)
        self.defocus_angle = 0.0
        self.focus_dist = 10.0
        self.background = Color(0.12, 0.12, 0.12)
        # These will be set in initialize()
        self.defocus_disk_u = Vec3(0, 0, 0)
        self.defocus_disk_v = Vec3(0, 0, 0)

    def initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        if self.image_height < 1:
            self.image_height = 1
        self.sqrt_spp = int(math.sqrt(self.samples_per_pixel))
        self.pixel_samples_scale = 1.0 / (self.sqrt_spp * self.sqrt_spp)
        self.recip_sqrt_spp = 1.0 / self.sqrt_spp
        self.center = self.lookfrom
        self.theta = math.radians(self.vfov)
        self.h = math.tan(self.theta / 2)
        self.viewport_height = 2.0 * self.h * self.focus_dist
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)
        self.w = Vec3.unit_vector(self.lookfrom - self.lookat)
        self.u = Vec3.unit_vector(Vec3.cross(self.vup, self.w))
        self.v = Vec3.cross(self.w, self.u)
        self.viewport_u = self.viewport_width * self.u
        self.viewport_v = self.viewport_height * -self.v
        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height
        self.viewport_upper_left = self.center - (self.focus_dist * self.w) - (self.viewport_u / 2) - (self.viewport_v / 2)
        self.pixel00_loc = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)
        self.defocus_radius = self.focus_dist * math.tan(math.radians(self.defocus_angle / 2))
        self.defocus_disk_u = self.u * self.defocus_radius
        self.defocus_disk_v = self.v * self.defocus_radius

    def render(self, file, world):
        start = datetime.datetime.now()
        self.initialize()
        file.write("P3\n")
        file.write(f"{self.image_width} {self.image_height}\n")
        file.write("255\n")
        for j in range(self.image_height):
            lines = self.image_height - j
            now = datetime.datetime.now()
            elapsed = now - start
            ect = ((elapsed / max(j, 1)) * lines)
            if j == 0:
                txt = f"Scanlines remaining: {lines}."
            else:
                txt = f"Scanlines remaining: {lines}.  Estimated complete in appx {ect} hh:mm:ss."
            print(txt)
            for i in range(self.image_width):
                pixel_color = Vec3(0.0, 0.0, 0.0)
                for s_j in range(self.sqrt_spp):
                    for s_i in range(self.sqrt_spp):
                        r = self.get_ray(i, j, s_i, s_j)
                        pixel_color += self.ray_color(r, self.max_depth, world)
                write_color(file, self.pixel_samples_scale * pixel_color)

    def ray_color(self, r, depth, world):
        # If we've exceeded the ray bounce limit, no more light is gathered.
        if depth <= 0:
            return Color(0.0, 0.0, 0.0)
        rec = HitRecord()
        # If the ray hits nothing, return the background color.
        if not world.hit(r, Interval(0.001, float('inf')), rec):
            return self.background

        if rec.mat is None:
            return Color(0.0, 0.0, 0.0)

        color_from_emission = rec.mat.emitted(r, rec, rec.u, rec.v, rec.p)

        # Scatter: attenuation, scattered ray, pdf_value
        scatter_result = rec.mat.scatter(r, rec)
        if not scatter_result[0]:
            return color_from_emission
        _, scattered, attenuation, _ = scatter_result

        # Use cosine-weighted PDF for surface scattering
        surface_pdf = CosinePdf(rec.normal)
        scattered = Ray(rec.p, surface_pdf.generate(), r.time())
        pdf_value = surface_pdf.value(scattered.direction())
        scattering_pdf = rec.mat.scattering_pdf(r, rec, scattered)
        color_from_scatter = (attenuation * scattering_pdf * self.ray_color(scattered, depth - 1, world)) / pdf_value

        return color_from_emission + color_from_scatter

    def get_ray(self, i, j, s_i=0, s_j=0):
        offset = self.sample_square_stratified(s_i, s_j)
        pixel_sample = self.pixel00_loc + ((i + offset.x()) * self.pixel_delta_u) + ((j + offset.y()) * self.pixel_delta_v)
        ray_origin = self.center if (self.defocus_angle <= 0) else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        ray_time = random.random()
        return Ray(ray_origin, ray_direction, ray_time)

    def sample_square(self):
        return Vec3(random.random() - 0.5, random.random() - 0.5, 0)

    def sample_square_stratified(self, s_i, s_j):
        px = ((s_i + random.random()) * self.recip_sqrt_spp) - 0.5
        py = ((s_j + random.random()) * self.recip_sqrt_spp) - 0.5
        return Vec3(px, py, 0)

    def defocus_disk_sample(self):
        p = Vec3.random_in_unit_disk()
        return self.center + (p[0] * self.defocus_disk_u) + (p[1] * self.defocus_disk_v)