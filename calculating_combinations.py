import math
import random
import numpy as np
import random

def scale_lines(lines, edgeLen):
    # scale the coordinates of the line segments based on the edge length
    return [[(x1 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)),
              y1 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))),
             (x2 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)),
              y2 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))]
            for (x1, y1), (x2, y2) in lines]

def generate_unique_combinations(num_samples, num_locations, num_colors):
    colors = [f'Color {i+1}' for i in range(num_colors)]
    combinations = set()
    while len(combinations) < num_samples:
        combination = tuple(random.choice(colors) for _ in range(num_locations))
        combinations.add(combination)
    return list(combinations)

def is_valid_combination(combination, points, radius):
    # loop through combinations and filter out based on radius constraint 
    assert(len(combination) == len(points))
    for i, (x1, y1) in enumerate(points):
        for j, (x2, y2) in enumerate(points):
            if i != j :
                if (combination[i] == combination[j]) and math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) < radius:
                    return False
    return True

def calculating_combinations(N, loc, p, radius, lines, div, edgeLen, num_samples=10000, num_trials=100):
    # scale the line segments
    scaled_lines = scale_lines(lines, edgeLen)

    # generate all points on the scaled lines
    points = []
    for line in scaled_lines:
        (x1, y1), (x2, y2) = line
        dx, dy = (x2 - x1) / (div + 1), (y2 - y1) / (div + 1)
        for i in range(1, div + 1):
            points.append((x1 + i * dx, y1 + i * dy))
    
    print(points)
    
    # raises error if the number of locations exceed the number of points
    if len(points) < loc:
        raise ValueError("Number of locations cannot exceed the number of available points.")
    
    valid_counts = []
    for _ in range(num_trials):
        print("running")
        valid_count = 0
        combinations = np.array(generate_unique_combinations(num_samples, loc, N))
        # loop through combinations and filter out based on percent constraint 
        for combination in combinations:
            # print(combination)
            unique, counts = np.unique(combination, return_counts=True)
            uniqueComb = dict(zip(unique, counts/loc))
            color_flag = all(uniqueComb[key] >= p for key in uniqueComb)
            if color_flag and is_valid_combination(combination, points, radius):
                valid_count += 1
        valid_counts.append(valid_count / num_samples)
    
    # calculate statistics 
    mean_valid_percentage = np.mean(valid_counts)
    std_dev_valid_percentage = np.std(valid_counts)
    confidence_interval = 1.96 * std_dev_valid_percentage / math.sqrt(num_trials)  # 95% CI
    
    return mean_valid_percentage, confidence_interval

hexagon_lines = [
    [(0.8660254037844386, 2), (0.0, 1.5)], 
    [(0.8660254037844386, 2), (1.7320508075688772, 1.5)], 
    [(1.7320508075688772, 1.5), (1.7320508075688772, 0.5)], 
    [(0.8660254037844386, 0), (1.7320508075688772, 0.5)], 
    [(0.0, 0.5), (0.8660254037844386, 0)], 
    [(0.0, 0.5), (0.0, 1.5)],
    [(0.8660254037844386, 2), (0.8660254037844386, 1)], 
    [(1.7320508075688772, 1.5), (0.8660254037844386, 1)], 
    [(1.7320508075688772, 0.5), (0.8660254037844386, 1)], 
    [(0.8660254037844386, 0), (0.8660254037844386, 1)], 
    [(0.0, 0.5), (0.8660254037844386, 1)], 
    [(0.0, 1.5), (0.8660254037844386, 1)]
]

rectangle_lines = [
    [(0, 0), (1, 0)], 
    [(1, 0), (2, 0)],
    [(0, 2.5), (1, 2.5)], 
    [(1, 2.5), (2, 2.5)],
    [(0, 5), (1, 5)], 
    [(1, 5), (2, 5)],
    [(0, 7.5), (1, 7.5)], 
    [(1, 7.5), (2, 7.5)],
    [(0, 10), (1, 10)], 
    [(1, 10), (2, 10)],
    [(0, 12.5), (1, 12.5)], 
    [(1, 12.5), (2, 12.5)]
]

# parameters
N = 3  # number of colors
loc = 36  # number of locations
p = 0.10  # min percent of each color
radius = 10  # min distance in nm between same colors
div = 3  # number of colors per segment
edgeLen = 33  # length of segment in nm
num_samples = 100000 # number of samples per trial
num_trials = 1 # number of trials

# hexagon
hexagon_mean, hexagon_ci = calculating_combinations(N, loc, p, radius, hexagon_lines, div, edgeLen, num_samples, num_trials)
print(f"Hexagon: {hexagon_mean * 100:.2f}% ± {hexagon_ci * 100:.2f}% valid combinations")

# rectangle
rectangle_mean, rectangle_ci = calculating_combinations(N, loc, p, radius, rectangle_lines, div, edgeLen, num_samples, num_trials)
print(f"Rectangle: {rectangle_mean * 100:.2f}% ± {rectangle_ci * 100:.2f}% valid combinations")
