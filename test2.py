import random


def generate_city_with_buildings(rows=15, cols=70, min_spacing=2, building_density=0.5):
    # Create a blank city grid
    city = [[" " for _ in range(cols)] for _ in range(rows)]

    # Helper function to draw a horizontal road
    def draw_horizontal_road(y, x_start, x_end):
        for x in range(x_start, x_end):
            city[y][x] = "─"

    # Helper function to draw a vertical road
    def draw_vertical_road(x, y_start, y_end):
        for y in range(y_start, y_end):
            city[y][x] = "│"

    # Helper function to place a building
    def place_building(top_left_y, top_left_x, height, width):
        for y in range(top_left_y, top_left_y + height):
            for x in range(top_left_x, top_left_x + width):
                if 0 <= y < rows and 0 <= x < cols and city[y][x] == " ":
                    city[y][x] = "█"

    # Randomly generate spaced positions
    def generate_positions(max_val, min_spacing):
        positions = []
        current = random.randint(0, min_spacing)
        while current < max_val:
            positions.append(current)
            current += random.randint(min_spacing + 1, min_spacing + 4)
        return positions

    # Generate road positions with irregular gaps
    horizontal_roads = generate_positions(rows, min_spacing)
    vertical_roads = generate_positions(cols, min_spacing)

    # Add horizontal roads with varying lengths
    for y in horizontal_roads:
        if random.choice([True, False]):  # Randomize complete or partial roads
            x_start = 0
            x_end = cols
        else:
            x_start = random.randint(0, cols // 3)
            x_end = random.randint(cols // 2, cols)
        draw_horizontal_road(y, x_start, x_end)

    # Add vertical roads with varying lengths
    for x in vertical_roads:
        if random.choice([True, False]):  # Randomize complete or partial roads
            y_start = 0
            y_end = rows
        else:
            y_start = random.randint(0, rows // 3)
            y_end = random.randint(rows // 2, rows)
        draw_vertical_road(x, y_start, y_end)

    # Add intersections
    for y in range(rows):
        for x in range(cols):
            if (
                city[y][x] == "─"
                and y > 0
                and y < rows - 1
                and city[y - 1][x] == "│"
                and city[y + 1][x] == "│"
            ):
                city[y][x] = "┼"
            elif (
                city[y][x] == "│"
                and x > 0
                and x < cols - 1
                and city[y][x - 1] == "─"
                and city[y][x + 1] == "─"
            ):
                city[y][x] = "┼"

    # Add buildings near roads
    total_buildings = int(
        building_density * rows * cols / 20
    )  # Adjust building count based on density
    for _ in range(total_buildings):
        # Define building size probabilities
        size_options = [
            (1, 1),
            (1, 1),
            (1, 1),  # 60% chance of 1x1
            (1, 1),  # 60% chance of 1x1
            (1, 1),  # 60% chance of 1x1
            (2, 1),
            (2, 2),  # 30% chance of 2x2
            (2, 2),  # 30% chance of 2x2
        ]  # 10% chance of 3x3
        height, width = random.choice(size_options)

        road_y = random.choice(horizontal_roads)
        road_x = random.choice(vertical_roads)

        # Randomize placement near road
        offset_y = random.choice([-height, 1])
        offset_x = random.choice([-width, 1])

        top_left_y = max(road_y + offset_y, 0)
        top_left_x = max(road_x + offset_x, 0)

        # Check if the area is clear and place the building
        clear_area = all(
            0 <= top_left_y + dy < rows
            and 0 <= top_left_x + dx < cols
            and city[top_left_y + dy][top_left_x + dx] == " "
            for dy in range(height)
            for dx in range(width)
        )
        if clear_area:
            place_building(top_left_y, top_left_x, height, width)

    # Print the grid
    for row in city:
        print("".join(row))


# Example usage: Generate a city grid with different densities
generate_city_with_buildings(building_density=0.99)  # High density
