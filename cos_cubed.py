import math
import random

def f(r2):
    z = 1 - r2
    cos_theta = z
    return cos_theta ** 3

def pdf():
    return 1.0 / (2.0 * math.pi)

def main():
    N = 1_000_000
    total = 0.0
    for _ in range(N):
        r2 = random.random()
        total += f(r2) / pdf()
    print(f"PI/2 = {math.pi / 2.0:.12f}")
    print(f"Estimate = {total / N:.12f}")

if __name__ == "__main__":
    main()