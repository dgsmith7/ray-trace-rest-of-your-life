import os
import math
import random
from Vec3 import Vec3, Point3, Color
from HittableList import HittableList
from Sphere import Sphere
from Camera import Camera
from Material import Lambertian, Metal, Dielectric
from Texture import CheckerTexture
from Quad import Quad
from BVH import BVHNode
import datetime
from Texture import ImageTexture

filename = "quads.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():
    world = HittableList()

    # Materials
    left_red = Lambertian(Color(1.0, 0.2, 0.2))
    back_green = Lambertian(Color(0.2, 1.0, 0.2))
    right_blue = Lambertian(Color(0.2, 0.2, 1.0))
    upper_orange = Lambertian(Color(1.0, 0.5, 0.0))
    lower_teal = Lambertian(Color(0.2, 0.8, 0.8))

    # Quads
    world.add(Quad(Point3(-3, -2, 5), Vec3(0, 0, -4), Vec3(0, 4, 0), left_red))
    world.add(Quad(Point3(-2, -2, 0), Vec3(4, 0, 0), Vec3(0, 4, 0), back_green))
    world.add(Quad(Point3(3, -2, 1), Vec3(0, 0, 4), Vec3(0, 4, 0), right_blue))
    world.add(Quad(Point3(-2, 3, 1), Vec3(4, 0, 0), Vec3(0, 0, 4), upper_orange))
    world.add(Quad(Point3(-2, -3, 5), Vec3(4, 0, 0), Vec3(0, 0, -4), lower_teal))

    cam = Camera()
    cam.aspect_ratio = 1
    cam.image_width = 400
    cam.samples_per_pixel = 25
    cam.max_depth = 25
    cam.vfov = 80
    cam.lookfrom = Point3(0, 0, 9)
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
