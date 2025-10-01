from Interval import Interval
import math

def linear_to_gamma(linear_component):
  if (linear_component > 0):
    return math.sqrt(linear_component)
  else:
    return 0

def write_color(file, pixelColor):
  r = pixelColor.x()
  g = pixelColor.y()
  b = pixelColor.z()

  # Apply a linear to gamma transform for gamma 2
  r = linear_to_gamma(r)
  g = linear_to_gamma(g)
  b = linear_to_gamma(b)

  # Translate the [0,1] component values to the byte range [0,255].
  intensity = Interval(0.000, 0.999)
  rbyte = int(256 * intensity.clamp(r))
  gbyte = int(256 * intensity.clamp(g))
  bbyte = int(256 * intensity.clamp(b))

  # Write out the pixel color components to ppm file.
  txt = f"{rbyte} {gbyte} {bbyte}   \n"
  file.write(txt)
