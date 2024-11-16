import heapq
import random

# Constants
GRID_SIZE = 20  # Size of the city grid
START_POINT = (GRID_SIZE // 2, GRID_SIZE // 2)  # Starting point for the city
DIRECTIONS = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}  # Possible road directions
ROAD_BRANCH_PROBABILITY = 0.3  # Probability of branching from an existing road segment
DENSITY_THRESHOLD = 0.8  # Higher density required for more road branches
ROAD_LENGTH = (
    5  # Number of segments a road continues in the same direction before branching
)

# Initialize grid
grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Priority queue to handle road segments
queue = []

# Track placed road segments
segments = set()

# Initialize population density map using random values
density_map = [[random.random() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


# Define Road Segment as a tuple (time, x, y, direction, remaining_length)
def add_road_segment(t, x, y, direction, remaining_length):
    if (x, y) not in segments:
        heapq.heappush(queue, (t, x, y, direction, remaining_length))


# Add the starting road segment to the queue
add_road_segment(
    0,
    START_POINT[0],
    START_POINT[1],
    random.choice(list(DIRECTIONS.keys())),
    ROAD_LENGTH,
)

# Main generation loop for roads
while queue:
    # Pop the segment with the lowest time (t)
    t, x, y, direction, remaining_length = heapq.heappop(queue)

    # Check if this segment is valid to add (i.e., not out of bounds or overlapping)
    if (x, y) in segments or not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
        continue

    # Add the segment to the grid and segment list
    segments.add((x, y))
    grid[x][y] = "+"  # Use '+' to represent road segments on the grid

    # If the road has remaining length, continue in the same direction
    if remaining_length > 0:
        dx, dy = DIRECTIONS[direction]
        add_road_segment(t + 1, x + dx, y + dy, direction, remaining_length - 1)
    else:
        # If no remaining length, consider branching to new directions
        for dir_key, (dx, dy) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy

            # Limit road branching based on density and probability
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (
                    dir_key == direction or density_map[nx][ny] > DENSITY_THRESHOLD
                ) and random.random() < ROAD_BRANCH_PROBABILITY:
                    add_road_segment(t + 1, nx, ny, dir_key, ROAD_LENGTH)


# Function to place buildings around roads
def place_buildings():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # Place a building if the cell is empty and adjacent to a road
            if grid[x][y] == " ":
                adjacent_to_road = any(
                    (x + dx, y + dy) in segments
                    for dx, dy in DIRECTIONS.values()
                    if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE
                )
                # Lower probability for building placement, to keep it sparse
                if adjacent_to_road and random.random() < 0.5:
                    grid[x][y] = "#"


# Place buildings around the roads
place_buildings()

# Print the grid
for row in grid:
    print(" ".join(row))
