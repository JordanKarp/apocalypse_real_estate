from random import choice, sample, randint
from location import Location
from map_constants import Buildings, Icons, Tile, ROAD_NAMES
from utility import list2d_get, colored, distance_points, extract_subgrid

MIN_ROAD_LENGTH = 3
MAP_COLUMNS = 90
MAP_ROWS = 12
VIEW_DISTANCE = 7
MAP_BUILDINGS = 140


class Map:
    def __init__(self, dimensions=(MAP_ROWS, MAP_COLUMNS)):
        self.dimensions = dimensions
        self.streets = {"vert": {}, "horiz": {}}
        self.buildings = []
        self.current_location = [4, 28]
        self.data = [[" " for _ in range(dimensions[1])] for _ in range(dimensions[0])]
        self.nearby = []

    @classmethod
    def new_map(cls, dimensions=(MAP_ROWS, MAP_COLUMNS), buildings=MAP_BUILDINGS):
        new_m = Map(dimensions)
        init_num_horiz = dimensions[0] // 5
        prev = 0
        for i in range(init_num_horiz):
            row_st = randint(prev, (i + 1) * (dimensions[0] // init_num_horiz))
            print(prev, (i + 1) * (dimensions[0] // init_num_horiz), row_st)
            if i == 0:
                col_st = 0
                length = dimensions[1] - col_st
            else:
                col_st = randint(1, dimensions[1] // 4)
                length = randint(dimensions[1] // 2, dimensions[1] - col_st)
            prev = row_st + MIN_ROAD_LENGTH
            new_m.add_road(False, row_st, col_st, length)

        init_num_vert = dimensions[1] // 20
        prev = 0
        for i in range(init_num_vert):
            row_st = randint(1, dimensions[0] // 4)
            col_st = randint(1, (i + 1) * (dimensions[1] // init_num_vert))
            if i == 0:
                row_st = 0
                length = dimensions[0] - row_st
            else:
                row_st = randint(1, dimensions[0] // 4)
                length = randint(dimensions[0] // 2, dimensions[0] - row_st)
            prev = col_st + MIN_ROAD_LENGTH
            new_m.add_road(True, row_st, col_st, length)

        new_m.add_buildings(MAP_BUILDINGS)

        return new_m

    def move_to(self, loc):
        self.current_location = loc

    def move(self, direction):
        if direction == "UP":
            self.current_location[0] -= 1
        elif direction == "DOWN":
            self.current_location[0] += 1
        elif direction == "LEFT":
            self.current_location[1] -= 1
        elif direction == "RIGHT":
            self.current_location[1] += 1

    def top_border_row(self, start=0, end=None):
        if end is None:
            end = self.dimensions[1]
        string = Icons.SINGLE_H_ROAD * self.dimensions[1]
        for num in self.streets["vert"]:
            one_more = num + 1
            string = string[:num] + self.streets["vert"][num][0] + string[one_more:]

        string = string[start:end]
        return Icons.SINGLE_TL_CORNER + string + Icons.SINGLE_TR_CORNER

    def bottom_border_row(self, length=None):
        if length is None:
            length = self.dimensions[1]
        return (
            Icons.SINGLE_BL_CORNER
            + Icons.SINGLE_H_ROAD * length
            + Icons.SINGLE_BR_CORNER
        )

    def add_road(self, is_vert, row_st, col_st, length, name=None):
        if not name:
            name = choice(ROAD_NAMES).title()
        if is_vert:
            self.add_vertical_road(row_st, col_st, length, name)
        else:
            self.add_horizontal_road(row_st, col_st, length, name)

    def add_vertical_road(self, row_st, col_st, length, name):
        if length:
            for _ in range(length):
                if list2d_get(self.data, row_st, col_st, None) == Icons.EMPTY:
                    self.data[row_st][col_st] = Tile(
                        Icons.V_ROAD, (row_st, col_st), name
                    )
                elif list2d_get(self.data, row_st, col_st, None) == Icons.H_ROAD:
                    self.data[row_st][col_st] = Tile(
                        Icons.CROSS, (row_st, col_st), name
                    )
                row_st += 1
            self.streets["vert"][col_st] = name

    def add_horizontal_road(self, row_st, col_st, length, name):
        if length:
            for _ in range(length):
                if list2d_get(self.data, row_st, col_st, None) == Icons.EMPTY:
                    self.data[row_st][col_st] = Tile(
                        Icons.H_ROAD, (row_st, col_st), name
                    )
                elif list2d_get(self.data, row_st, col_st, None) == Icons.V_ROAD:
                    self.data[row_st][col_st] = Tile(
                        Icons.CROSS, (row_st, col_st), name
                    )
                col_st += 1
            self.streets["horiz"][row_st] = name

    def determine_eligible_spots(self, num_eligible_spots=1):
        eligible_spots = []
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if self.data[row][col] == Icons.EMPTY:
                    neighbors = self.get_neighbors(row, col)
                    # if len(neighbors) in [0, 1, 2, 3, 4, 5, 6]:

                    # is_even = False
                    # if (
                    #     neighbors[0].grid_loc[0] > row
                    #     or neighbors[0].grid_loc[1] > col
                    # ):
                    #     is_even = True
                    # if neighbors[0].icon == Icons.H_ROAD:
                    #     num = col * 2 if is_even else col * 2 + 1
                    # else:
                    #     num = row * 2 if is_even else row * 2 + 1
                    # name = f"{num} {neighbors[0].name}"
                    name = min(len(neighbors), 9)
                    eligible_spots.append((row, col, name))
        return eligible_spots

    def add_buildings(self, num_buildings):
        # get all eligible spots
        # for each eligible spot
        #   choose a building based on building probabilities

        eligible_spots = self.determine_eligible_spots()
        buildings = list(Buildings)
        # for spot in sample(eligible_spots, num_buildings):
        for spot in eligible_spots:

            building = Tile(choice(buildings), (spot[0], spot[1]), spot[2])
            location = Location(
                spot[2], occupied=False, name="HOUSETYPE", floors="FLOORS"
            )
            self.buildings.append(location)
            # self.data[spot[0]][spot[1]] = building
            self.data[spot[0]][spot[1]] = spot[2]

    # def remove_neighbors(self, eligible_spots, spot):
    #     if (spot[0] - 1, spot[1]) in eligible_spots:
    #         eligible_spots.remove((spot[0] - 1, spot[1]))
    #     elif (spot[0] + 1, spot[1]) in eligible_spots:
    #         eligible_spots.remove((spot[0] + 1, spot[1]))
    #     elif (spot[0], spot[1] - 1) in eligible_spots:
    #         eligible_spots.remove((spot[0], spot[1] - 1))
    #     elif (spot[0], spot[1] + 1) in eligible_spots:
    #         eligible_spots.remove((spot[0], spot[1] + 1))

    def get_neighbors(self, row, col):
        neighbors = []
        pairs = [
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        ]
        for n_row, n_col in pairs:
            if list2d_get(self.data, n_row, n_col, Icons.EMPTY) != Icons.EMPTY:
                neighbors.append(self.data[n_row][n_col])

        return neighbors

    def sort_key(self, tile):
        # Split the name into parts
        parts = tile.address.split(" ", 1)  # Split into number and street name
        number = int(parts[0])  # First part is the number, convert to int
        street = parts[1]  # Second part is the street name
        return (street, number)

    def draw_partial_map(self, row_st, row_end, col_st, col_end):
        data = extract_subgrid(self.data, row_st, row_end, col_st, col_end)

        # ! TODO FIX
        adjusted_location = [
            self.current_location[0] - row_st,
            self.current_location[1] - col_st,
        ]

        self.nearby = []
        print("The Map".center(col_end - col_st))
        print(self.top_border_row(col_st, col_end))
        for row_num, row in enumerate(data):
            char = Icons.SINGLE_V_ROAD
            if row_num in self.streets["horiz"]:
                char = self.streets["horiz"][row_num][0]
            print(char, end="")
            for col_num, col in enumerate(row):

                if [row_num, col_num] == adjusted_location:
                    print(colored("⭑", "red"), end="")
                # elif (
                #     distance_points(adjusted_location, (row_num, col_num))
                #     > VIEW_DISTANCE
                # ):
                #     print("░", end="")
                elif isinstance(col, Tile):
                    print(col.icon, end="")
                    if col.icon in Buildings:
                        self.nearby.append(col)
                else:
                    print(col, end="")

            print(Icons.SINGLE_V_ROAD)
        print(self.bottom_border_row(col_end - col_st))

        for elem in self.nearby:
            print(elem.name)

    def draw_map(self):
        self.draw_partial_map(0, self.dimensions[0], 0, self.dimensions[1])


# new = Map((15, 90)).new_map()
# new.draw_map()
