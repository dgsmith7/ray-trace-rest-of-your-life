import math
from Vec3 import Vec3

def f(d: Vec3) -> float:
    cos_theta = d.z()
    return cos_theta ** 3

def pdf(d: Vec3) -> float:
    return d.z() / math.pi

def main():
    N = 1_000_000
    total = 0.0
    for _ in range(N):
        d = Vec3.random_cosine_direction()
        total += f(d) / pdf(d)
    print(f"PI/2 = {math.pi / 2.0:.12f}")
    print(f"Estimate = {total / N:.12f}")

if __name__ == "__main__":
    main()