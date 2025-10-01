import os
from Vec3 import Vec3, Point3, Color
from HittableList import HittableList
from Sphere import Sphere
from Camera import Camera
from Material import Lambertian, Metal, Dielectric
import math
import random
import datetime
from terrain import elevation

filename = "planetTest.ppm"

# World
world = HittableList()

planetMat1 = Metal(Color(0.82, 0.427, 0.29), 1.0)
world.add(Sphere(Point3(0,0,0), 5, planetMat1))
planetMat2 = Dielectric(1.3/1.5)
world.add(Sphere(Point3(0,0,0), 5.2, planetMat2))

sunMat = Metal(Color(1.0, 1.0, 1.0), 0.0)
world.add(Sphere(Point3(-100,0,100), 25, sunMat))

for i in range(150):
  iceMat = Dielectric(2.65)
  ang = random.random() * (math.pi*2)
  dist = random.random() *3 + 8
  world.add(Sphere(Point3(math.cos(ang)*dist,0,math.sin(ang)*dist), random.random() * 0.05, iceMat))

for i in range(150):
  rockMat = Lambertian(Color(0.396, 0.18, 0.541))
  ang = random.random() * (math.pi*2)
  dist = random.random() *4 + 12
  world.add(Sphere(Point3(math.cos(ang)*dist,0,math.sin(ang)*dist), random.random() * 0.1, rockMat))

for i in range(150):
  crystalMat = Metal(Color(0.62, 0.6, 0.769), 0)
  ang = random.random() * (math.pi*2)
  dist = random.random() *5 + 15
  world.add(Sphere(Point3(math.cos(ang)*dist,0,math.sin(ang)*dist), random.random() * 0.07, crystalMat))

cam = Camera()
cam.aspect_ratio = 16.0 / 9.0 # Ratio of image width over height
cam.image_width = 1200 # Rendered image width in pixel count
cam.samples_per_pixel = 25 # Count of random samples for each pixel
cam.max_depth = 25 # Maximum number of ray bounces into scene.  
cam.vfov = 35 # Vertical view angle (field of view)
cam.lookfrom = Point3(9, 2, 10)
cam.lookat = Point3(-13, -0.2, 0)
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
  print("Finished rendering at: ", endtime)
  print("The render took: ", endtime-starttime)
  print("Done.\n")
  
def openNewImageFile():
  if os.path.exists(filename):
    os.remove(filename)
  return open(filename, "a")

main()