import os
from Vec3 import Vec3, Point3, Color
from HittableList import HittableList
from Sphere import Sphere
from Camera import Camera
from Material import Lambertian, Metal, Dielectric
import math
import random
import datetime
from stanfordTeapot import teapot

filename = "teapot2.ppm"

# World
world = HittableList()

#mat = Metal(Color(0.1, 0.1, 0.83), 1)

for i in range(3644):
    x=teapot[i*3]
    y=teapot[i*3+1]
    z=teapot[i*3+2]
    mat = Metal(Color(0.25, 0.25, (z/3.15) + 0.5), 1)
    world.add(Sphere(Point3(x,y,z), 0.075, mat))

mat2 = Dielectric(1.5)
world.add(Sphere(Point3(0,2,0), 0.5, mat2))
material_ground = Lambertian(Color(0.8, 0.6, 0.0))
world.add(Sphere(Point3( 0.0, -100.5, -1.0), 99.0, material_ground))

bgMat = Lambertian(Color(.7, .7, .7))
world.add(Sphere(Point3(-100,-20,-100), 85, bgMat))

cam = Camera()

cam.aspect_ratio = 16.0 / 9.0 # Ratio of image width over height
cam.image_width = 400 # Rendered image width in pixel count
cam.samples_per_pixel = 10 # Count of random samples for each pixel
cam.max_depth = 10 # Maximum number of ray bounces into scene.  Keep below 48.
cam.vfov = 35 # Vertical view angle (field of view)
cam.lookfrom = Point3(7, 5, 7)
cam.lookat = Point3(0, 2, 0)
cam.vup = Vec3(0, 1, 0)
cam.defocus_angle = 0.0
cam.focus_dist = 10.0

def main():
  # Render and write image to file
  starttime = datetime.datetime.now()
  print("Started rendering at: ", starttime)
  f = openNewImageFile()
  cam.render(f, world)
  f.close()
  endtime = datetime.datetime.now()
  print("Finisheded rendering at: ", endtime)
  print("The render took: ", endtime-starttime)
  print("Done.\n")
  
def openNewImageFile():
  if os.path.exists(filename):
    os.remove(filename)
  return open(filename, "a")

main()