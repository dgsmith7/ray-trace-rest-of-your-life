import os
import math
import random
from Vec3 import Vec3, Point3, Color
from HittableList import HittableList
from Sphere import Sphere
from Camera import Camera
from Material import Lambertian, Metal, Dielectric
from BVH import BVHNode
import datetime

filename = "bouncingSphere.ppm"

def random_color():
    return Color(random.random(), random.random(), random.random())

def main():
    world = HittableList()

    # Ground
    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    # Random spheres
    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Point3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())
            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # Diffuse (Lambertian)
                    albedo = random_color() * random_color()
                    sphere_material = Lambertian(albedo)
                    center2 = center + Vec3(0, random.uniform(0, 0.5), 0)
                    world.add(Sphere(center, 0.2, sphere_material, center2=center2))
                elif choose_mat < 0.95:
                    # Metal
                    albedo = Color(random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # Dielectric (glass)
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))


    # Three big spheres
    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

    # Wrap world in BVH
    world = HittableList(BVHNode(world))

    cam = Camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 400
    cam.samples_per_pixel = 25
    cam.max_depth = 25
    cam.vfov = 20
    cam.lookfrom = Point3(13, 2, 3)
    cam.lookat = Point3(0, 0, 0)
    cam.vup = Vec3(0, 1, 0)
    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0

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
