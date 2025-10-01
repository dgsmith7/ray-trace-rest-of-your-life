import os
import math
import random
from Vec3 import Vec3, Point3, Color
from HittableList import HittableList
from Sphere import Sphere
from Camera import Camera
from Material import Lambertian, Metal, Dielectric
from Texture import CheckerTexture
from BVH import BVHNode
import datetime
from Texture import ImageTexture

filename = "imageTexture.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():
    world = HittableList()

    # Earth texture mapped sphere
    earth_texture = ImageTexture("/Users/dgsmith7/Documents/Education/Software Engineering/Fall 2025/Directed Study/ray-trace-next-week/RTW_IMAGES/earthmap.jpg")
    earth_surface = Lambertian(earth_texture)
    globe = Sphere(Point3(0, 0, 0), 2, earth_surface)
    world.add(globe)

    cam = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 25
    cam.max_depth = 25
    cam.vfov = 20
    cam.lookfrom = Point3(0, 0, 12)
    cam.lookat = Point3(0, 0, 0)
    cam.vup = Vec3(0, 1, 0)
    cam.defocus_angle = 0

    starttime = datetime.datetime.now()
    print("Started rendering at: ", starttime)
    f = open_new_image_file()
    cam.render(f, world)
    f.close()
    endtime = datetime.datetime.now()
    print("Finished rendering at: ", endtime)
    print("The render took: ", endtime - starttime)
    print("Done.\n")

def open_new_image_file():
    if os.path.exists(filename):
        os.remove(filename)
    return open(filename, "a")

if __name__ == "__main__":
    main()
