# NoiseTexture: procedural texture using Perlin noise
from Perlin import Perlin
import math
from Vec3 import Color
from Rtw_image import RtwImage
from Interval import Interval

class Texture:
    def value(self, u, v, p):
        """
        Abstract method to get the color value at texture coordinates (u, v) and point p.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Texture subclasses must implement the value method.")

class SolidColor(Texture):
    def __init__(self, albedo):
        if isinstance(albedo, Color):
            self.albedo = albedo
        else:
            # Accepts tuple/list or individual RGB values
            self.albedo = Color(*albedo)

    def value(self, u, v, p):
        return self.albedo

# CheckerTexture: supports both (scale, even, odd) and (scale, c1, c2) signatures
class CheckerTexture(Texture):
    def __init__(self, scale, even, odd=None):
        self.inv_scale = 1.0 / scale if scale != 0 else 1.0
        if odd is None:
            # If only two colors are given, treat as (scale, c1, c2)
            self.even = SolidColor(even)
            self.odd = SolidColor(scale)
        else:
            self.even = even if isinstance(even, Texture) else SolidColor(even)
            self.odd = odd if isinstance(odd, Texture) else SolidColor(odd)

    def value(self, u, v, p):
        x_int = int(math.floor(self.inv_scale * p.x()))
        y_int = int(math.floor(self.inv_scale * p.y()))
        z_int = int(math.floor(self.inv_scale * p.z()))
        is_even = (x_int + y_int + z_int) % 2 == 0
        return self.even.value(u, v, p) if is_even else self.odd.value(u, v, p)
    
class ImageTexture(Texture):
    def __init__(self, filename):
        self.image = RtwImage(filename)

    def value(self, u, v, p):
        # If we have no texture data, return solid cyan as a debugging aid
        if self.image.height() <= 0:
            return Color(0, 1, 1)
        # Clamp input texture coordinates to [0,1] x [1,0]
        u_clamped = Interval(0, 1).clamp(u)
        v_clamped = 1.0 - Interval(0, 1).clamp(v)  # Flip V to image coordinates
        i = int(u_clamped * self.image.width())
        j = int(v_clamped * self.image.height())
        pixel = self.image.pixel_data(i, j)
        color_scale = 1.0 / 255.0
        return Color(color_scale * pixel[0], color_scale * pixel[1], color_scale * pixel[2])

class NoiseTexture(Texture):
    def __init__(self, scale=1.0):
        self.noise = Perlin()
        self.scale = scale

    def value(self, u, v, p):
        # Marble-like pattern: sin(scale * p.z() + 10 * turbulence)
        t = self.noise.turb(p, 7)
        marble = math.sin(self.scale * p.z() + 10 * t)
        return Color(0.5, 0.5, 0.5) * (1 + marble)
