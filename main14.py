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

filename = "finalScene.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():

    # Grid of boxes with random heights (ground)
    boxes1 = HittableList()
    ground = Lambertian(Color(0.48, 0.83, 0.53))
    boxes_per_side = 20
    w = 100.0
    for i in range(boxes_per_side):
        for j in range(boxes_per_side):
            x0 = -1000.0 + i * w
            z0 = -1000.0 + j * w
            y0 = 0.0
            x1 = x0 + w
            y1 = random.uniform(1, 101)
            z1 = z0 + w
            boxes1.add(box(Point3(x0, y0, z0), Point3(x1, y1, z1), ground))

    world = HittableList()

    # Add BVH of ground boxes
    world.add(BVHNode(boxes1.objects))

    # Light
    light = DiffuseLight(Color(7, 7, 7))
    world.add(Quad(Point3(123, 554, 147), Vec3(300, 0, 0), Vec3(0, 0, 265), light))

    # Moving sphere
    center1 = Point3(400, 400, 200)
    center2 = center1 + Vec3(30, 0, 0)
    sphere_material = Lambertian(Color(0.7, 0.3, 0.1))
    world.add(Sphere(center1, 50, sphere_material, center2=center2))

    # Glass sphere
    world.add(Sphere(Point3(260, 150, 45), 50, Dielectric(1.5)))

    # Metal sphere
    world.add(Sphere(Point3(0, 150, 145), 50, Metal(Color(0.8, 0.8, 0.9), 1.0)))

    # Foggy glass sphere
    boundary = Sphere(Point3(360, 150, 145), 70, Dielectric(1.5))
    world.add(boundary)
    world.add(ConstantMedium(boundary, 0.2, Color(0.2, 0.4, 0.9)))

    # Global fog
    boundary2 = Sphere(Point3(0, 0, 0), 5000, Dielectric(1.5))
    world.add(ConstantMedium(boundary2, 0.0001, Color(1, 1, 1)))

    # Earth texture sphere
    earth_texture = ImageTexture("/Users/dgsmith7/Documents/Education/Software Engineering/Fall 2025/Directed Study/ray-trace-next-week/RTW_IMAGES/earthmap.jpg")
    emat = Lambertian(earth_texture)
    world.add(Sphere(Point3(400, 200, 400), 100, emat))

    # Perlin noise sphere
    pertext = NoiseTexture(0.2)
    world.add(Sphere(Point3(220, 280, 300), 80, Lambertian(pertext)))

    # Cluster of small spheres
    boxes2 = HittableList()
    white = Lambertian(Color(0.73, 0.73, 0.73))
    ns = 1000
    for j in range(ns):
        center = Point3(random.uniform(0, 165), random.uniform(0, 165), random.uniform(0, 165))
        boxes2.add(Sphere(center, 10, white))
    cluster = BVHNode(boxes2.objects)
    cluster = RotateY(cluster, 15)
    cluster = Translate(cluster, Vec3(-100, 270, 395))
    world.add(cluster)

    cam = Camera()
    cam.aspect_ratio = 1.0
    cam.image_width = 400#800
    cam.samples_per_pixel = 250#10000
    cam.max_depth = 4#40
    cam.background = Vec3(0, 0, 0)
    cam.vfov = 40
    cam.lookfrom = Point3(278, 278, -600)
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
