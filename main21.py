import os
import math
import random
from Vec3 import Vec3, Point3, Color
from HittableList import HittableList
from Hittable import RotateY, Translate
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
from Texture import ImageTexture, NoiseTexture

filename = "cornell_box_orthonormal.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():

    # Cornell box scene
    world = HittableList()
    red = Lambertian(Color(.65, .05, .05))
    white = Lambertian(Color(.73, .73, .73))
    green = Lambertian(Color(.12, .45, .15))
    light = DiffuseLight(Color(15, 15, 15))
    
    # Cornell box sides
    world.add(Quad(Point3(555,0,0), Vec3(0,0,555), Vec3(0,555,0), green))
    world.add(Quad(Point3(0,0,555), Vec3(0,0,-555), Vec3(0,555,0), red))
    world.add(Quad(Point3(0,555,0), Vec3(555,0,0), Vec3(0,0,555), white))
    world.add(Quad(Point3(0,0,555), Vec3(555,0,0), Vec3(0,0,-555), white))
    world.add(Quad(Point3(555,0,555), Vec3(-555,0,0), Vec3(0,555,0), white))
    
    # Light
    world.add(Quad(Point3(213,554,227), Vec3(130,0,0), Vec3(0,0,105), light))
    
    # Box 1
    box1 = box(Point3(0,0,0), Point3(165,330,165), white)
    box1 = RotateY(box1, 15)
    box1 = Translate(box1, Vec3(265,0,295))
    world.add(box1)
    
    # Box 2
    box2 = box(Point3(0,0,0), Point3(165,165,165), white)
    box2 = RotateY(box2, -18)
    box2 = Translate(box2, Vec3(130,0,65))
    world.add(box2)

    # Use BVH for acceleration
    world = BVHNode(world.objects, 0, len(world.objects))

    cam = Camera()
    cam.aspect_ratio = 1.0
    cam.image_width = 600
    cam.samples_per_pixel = 100
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
