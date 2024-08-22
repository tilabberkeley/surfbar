import math
import random
import numpy as np

def scale_lines(lines, edgeLen):
    return [[(x1 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)),
              y1 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))),
             (x2 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)),
              y2 * (edgeLen / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)))]
            for (x1, y1), (x2, y2) in lines]

def generate_color_location_combinations(num_samples, points, num_colors):

    colors = [f'Color {i+1}' for i in range(num_colors)]
    combinations = set()  

    while len(combinations) <= num_samples:
        color_assignment = tuple(sorted((random.choice(colors), point) for point in random.sample(points, len(points))))
        combinations.add(color_assignment)
    
    return list(combinations)

def is_valid_combination(combination, radius):

    for i in range(len(combination)):
        color_i, (x1, y1) = combination[i]
        for j in range(i + 1, len(combination)):
            color_j, (x2, y2) = combination[j]
            if color_i == color_j:
                if math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= radius:
                    return False
    return True

def calculating_combinations(N, loc, p, radius, lines, div, edgeLen, num_samples, num_trials):
    
    scaled_lines = scale_lines(lines, edgeLen)
    
    # generate the points where colors can be placed on the DNA Origami surface
    points = []
    for line in scaled_lines:
        (x1, y1), (x2, y2) = line
        dx, dy = (x2 - x1) / (div + 1), (y2 - y1) / (div + 1)
        for i in range(1, div + 1):
            points.append((x1 + i * dx, y1 + i * dy))
    
    # ensure that the number of locations does not exceed the available points
    if len(points) < loc:
        raise ValueError("Number of locations cannot exceed the number of available points.")
    
    valid_counts = []
    for _ in range(num_trials):
        print("running")
        valid_count = 0
        
        # generate a list of unique color-location combinations
        combinations = generate_color_location_combinations(num_samples, points, N)
        
        for combination in combinations:
            # calculate the proportion of each color in the combination
            color_counts = {color: 0 for color in set([color for color, _ in combination])}
            for color, _ in combination:
                color_counts[color] += 1
            color_proportions = {color: count / loc for color, count in color_counts.items()}
            
            # check if all color proportions meet the minimum percentage constraint
            color_flag = all(proportion >= p for proportion in color_proportions.values())
            
            # check if the combination is valid according to the radius constraint
            if color_flag and is_valid_combination(combination, radius):
                valid_count += 1
        
        valid_counts.append(valid_count / num_samples)
    
    # calculate the mean percentage of valid combinations and the confidence interval
    mean_valid_percentage = np.mean(valid_counts)
    std_dev_valid_percentage = np.std(valid_counts)
    confidence_interval = 1.96 * std_dev_valid_percentage / math.sqrt(num_trials)
    
    return mean_valid_percentage, confidence_interval

# Parameters
N = 3  # number of colors
loc = 36  # number of locations
p = 0.25  # min percent of each color
radius = 2  # min distance in nm between same colors
div = 3  # number of points per segment
edgeLen = 33  # length of segment in nm
num_samples = 100000  # number of samples per trial
num_trials = 10  # number of trials

# lines representing the hexagon and rectangle
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
    [(0, 0 / edgeLen), (1, 0 / edgeLen)], 
    [(1, 0 / edgeLen), (2, 0 / edgeLen)],
    [(0, 2.5 / edgeLen), (1, 2.5 / edgeLen)], 
    [(1, 2.5 / edgeLen), (2, 2.5 / edgeLen)],
    [(0, 5 / edgeLen), (1, 5 / edgeLen)], 
    [(1, 5 / edgeLen), (2, 5 / edgeLen)],
    [(0, 7.5 / edgeLen), (1, 7.5 / edgeLen)], 
    [(1, 7.5 / edgeLen), (2, 7.5 / edgeLen)],
    [(0, 10 / edgeLen), (1, 10 / edgeLen)], 
    [(1, 10 / edgeLen), (2, 10 / edgeLen)],
    [(0, 12.5 / edgeLen), (1, 12.5 / edgeLen)], 
    [(1, 12.5 / edgeLen), (2, 12.5 / edgeLen)]
]


# Hexagon
hexagon_mean, hexagon_ci = calculating_combinations(N, loc, p, radius, hexagon_lines, div, edgeLen, num_samples, num_trials)
print(f"Hexagon: {hexagon_mean * 100:.2f}% ± {hexagon_ci * 100:.2f}% valid combinations")

# Rectangle
rectangle_mean, rectangle_ci = calculating_combinations(N, loc, p, radius, rectangle_lines, div, edgeLen, num_samples, num_trials)
print(f"Rectangle: {rectangle_mean * 100:.2f}% ± {rectangle_ci * 100:.2f}% valid combinations")
