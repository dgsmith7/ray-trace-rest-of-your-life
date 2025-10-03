import random
import math

def icd(d):
    """Inverse cumulative distribution function"""
    return 8.0 * pow(d, 1.0/3.0)

def pdf(x):
    """Probability density function"""
    return (3.0/8.0) * x * x

def main():
    N = 1
    sum_val = 0.0
    
    for i in range(N):
        z = random.random()
        if z == 0.0:  # Ignore zero to avoid NaNs
            continue
        x = icd(z)
        sum_val += x * x / pdf(x)
    
    print(f"I = {sum_val / N:.12f}")

if __name__ == "__main__":
    main()
