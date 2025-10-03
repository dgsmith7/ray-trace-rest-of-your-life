import random
import math
from Vec3 import Vec3

def f(d):
    """Function to integrate: cosine squared"""
    cosine_squared = d.z() * d.z()
    return cosine_squared

def pdf(d):
    """Probability density function for uniform sampling on unit sphere"""
    pi = math.pi
    return 1 / (4 * pi)

def random_unit_vector():
    """Generate a random unit vector (copied from Vec3 since it's not properly marked as static)"""
    while True:
        p = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        lensq = p.length_squared()
        if 1e-160 < lensq <= 1.0:
            return p / math.sqrt(lensq)

def main():
    N = 1000000
    sum_val = 0.0
    
    for i in range(N):
        d = random_unit_vector()
        f_d = f(d)
        sum_val += f_d / pdf(d)
    
    print(f"I = {sum_val / N:.12f}")

if __name__ == "__main__":
    main()
