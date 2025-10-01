import random

def main():
    inside_circle = 0
    inside_circle_stratified = 0
    sqrt_N = 1000
    
    for i in range(sqrt_N):
        for j in range(sqrt_N):
            # Regular random sampling
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x*x + y*y < 1:
                inside_circle += 1
            
            # Stratified sampling
            x = 2*((i + random.random()) / sqrt_N) - 1
            y = 2*((j + random.random()) / sqrt_N) - 1
            if x*x + y*y < 1:
                inside_circle_stratified += 1
    
    total_samples = sqrt_N * sqrt_N
    regular_estimate = (4.0 * inside_circle) / total_samples
    stratified_estimate = (4.0 * inside_circle_stratified) / total_samples
    
    print(f"Regular Estimate of Pi = {regular_estimate:.12f}")
    print(f"Stratified Estimate of Pi = {stratified_estimate:.12f}")

if __name__ == "__main__":
    main()