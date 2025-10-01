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
from Material import DiffuseLight

filename = "simeplLight2.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():
    world = HittableList()

    # Perlin noise texture mapped spheres
    from Texture import NoiseTexture
    pertext = NoiseTexture(4)
    noise_mat = Lambertian(pertext)
    world.add(Sphere(Point3(0, -1000, 0), 1000, noise_mat))
    world.add(Sphere(Point3(0, 2, 0), 2, noise_mat))

    # Add a diffuse light quad
    difflight = DiffuseLight(Color(4, 4, 4))
    world.add(Quad(Point3(3, 1, -2), Vec3(2, 0, 0), Vec3(0, 2, 0), difflight))

    # Add a diffuse light sphere
    world.add(Sphere(Point3(0, 7, 0), 2, difflight))

    cam = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 25
    cam.max_depth = 25
    cam.background = Vec3(0, 0, 0);
    cam.vfov = 20
    cam.lookfrom = Point3(26, 3, 6)
    cam.lookat = Point3(0, 2, 0)
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
