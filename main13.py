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
from Quad import box
from ConstantMedium import ConstantMedium

filename = "volumes.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():
    world = HittableList()

    # Cornell Box materials
    red = Lambertian(Color(0.65, 0.05, 0.05))
    white = Lambertian(Color(0.73, 0.73, 0.73))
    green = Lambertian(Color(0.12, 0.45, 0.15))
    light = DiffuseLight(Color(15, 15, 15))

    # Cornell Box quads
    world.add(Quad(Point3(555, 0, 0), Vec3(0, 555, 0), Vec3(0, 0, 555), green))
    world.add(Quad(Point3(0, 0, 0), Vec3(0, 555, 0), Vec3(0, 0, 555), red))
    world.add(Quad(Point3(343, 554, 332), Vec3(-130, 0, 0), Vec3(0, 0, -105), light))
    world.add(Quad(Point3(0, 0, 0), Vec3(555, 0, 0), Vec3(0, 0, 555), white))
    world.add(Quad(Point3(555, 555, 555), Vec3(-555, 0, 0), Vec3(0, 0, -555), white))
    world.add(Quad(Point3(0, 0, 555), Vec3(555, 0, 0), Vec3(0, 555, 0), white))

    # Add two white boxes to the Cornell Box
    from Hittable import RotateY, Translate
    # Box 1
    box1 = box(Point3(0, 0, 0), Point3(165, 330, 165), white)
    box1 = RotateY(box1, 15)
    box1 = Translate(box1, Vec3(265, 0, 295))
     # Box 2
    box2 = box(Point3(0, 0, 0), Point3(165, 165, 165), white)
    box2 = RotateY(box2, -18)
    box2 = Translate(box2, Vec3(130, 0, 65))
 
    world.add(ConstantMedium(box1, 0.01, Vec3(0, 0, 0)))
    world.add(ConstantMedium(box2, 0.01, Vec3(1, 1, 1)))

    cam = Camera()
    cam.aspect_ratio = 1.0
    cam.image_width = 600
    cam.samples_per_pixel = 200
    cam.max_depth = 50
    cam.background = Vec3(0, 0, 0)
    cam.vfov = 40
    cam.lookfrom = Point3(278, 278, -800)
    cam.lookat = Point3(278, 278, 0)
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
