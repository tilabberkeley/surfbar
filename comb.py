import random
import math

def generate_color_combinations(coordinates, colors, min_radius, num_combinations):
    unique_combinations = set()

    while len(unique_combinations) < num_combinations:
        assigned_colors = {coord: 0 for coord in coordinates}
        color_assigned = {coord: False for coord in coordinates}

        def distance(coord1, coord2):
            return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

        def is_valid_assignment(new_color, coord):
            for other_coord in coordinates:
                if color_assigned[other_coord]:  
                    if assigned_colors[other_coord] == new_color:
                        if distance(coord, other_coord) < min_radius:
                            return False
            return True

        combination_valid = True
        for coord in coordinates:
            temp_failed_colors = []  
            while len(temp_failed_colors) < len(colors):
                new_color = random.choice([c for c in colors if c not in temp_failed_colors])
                if is_valid_assignment(new_color, coord):
                    assigned_colors[coord] = new_color
                    color_assigned[coord] = True
                    break 
                else:
                    temp_failed_colors.append(new_color)

            if not color_assigned[coord]:
                combination_valid = False
                break

        if combination_valid:
            combination_tuple = tuple(sorted(assigned_colors.items()))
            
            if combination_tuple not in unique_combinations:
                unique_combinations.add(combination_tuple)
                
                print(f"\nCombination {len(unique_combinations)}:")
                color_count = {color: 0 for color in colors}
                for coord, color in assigned_colors.items():
                    print(f"Coordinate {coord}: Color {color}")
                    if color != 0:
                        color_count[color] += 1

                color_percentage = {color: (count / len(coordinates)) * 100 for color, count in color_count.items()}
                print("Color percentages:", color_percentage)

    return list(unique_combinations)

coordinates = [
    (8.25,0), (8.25,9.6), (8.25,19.2), (8.25,28.8), (8.25,38.4), (8.25,48),
    (16.5,0), (16.5,9.6), (16.5,19.2), (16.5,28.8), (16.5,38.4), (16.5,48),
    (24.75,0), (24.75,9.6), (24.75,19.2), (24.75,28.8), (24.75,38.4), (24.75,48),
    (41.25,0), (41.25,9.6), (41.25,19.2), (41.25,28.8), (41.25,38.4), (41.25,48),
    (49.5,0), (49.5,9.6), (49.5,19.2), (49.5,28.8), (49.5,38.4), (49.5,48),
    (57.75,0), (57.75,9.6), (57.75,19.2), (57.75,28.8), (57.75,38.4), (57.75,48)
]

colors = [1, 2, 3]  # number of colors
min_radius = 10  # minimum distance requirement
num_combinations = 5  # number of unique combinations to generate

generate_color_combinations(coordinates, colors, min_radius, num_combinations)