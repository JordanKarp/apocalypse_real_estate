from random import choice, sample
from location import Location
from map_constants import Buildings, Icons, Tile, ROAD_NAMES
from utility import list2d_get, colored, distance_points

MIN_ROAD_LENGTH = 3
MAP_COLUMNS = 90
MAP_ROWS = 15
VIEW_DISTANCE = 80


class Map:
    def __init__(self, dimensions=(MAP_ROWS, MAP_COLUMNS)):
        self.dimensions = dimensions
        self.streets = {"vert": {}, "horiz": {}}
        self.buildings = []
        self.current_location = [4, 28]
        self.data = [[" " for _ in range(dimensions[1])] for _ in range(dimensions[0])]

    def move_to(self, loc):
        self.current_location = loc

    def move(self, direction):
        if direction == "UP":
            self.current_location[0] -= 1
        if direction == "DOWN":
            self.current_location[0] += 1
        if direction == "LEFT":
            self.current_location[1] -= 1
        if direction == "RIGHT":
            self.current_location[1] += 1

    @property
    def top_border_row(self):
        string = Icons.SINGLE_H_ROAD * self.dimensions[1]
        for num in self.streets["vert"]:
            string = string[:num] + self.streets["vert"][num][0] + string[num + 1 :]

        return Icons.SINGLE_TL_CORNER + string + Icons.SINGLE_TR_CORNER

    @property
    def bottom_border_row(self):
        return (
            Icons.SINGLE_BL_CORNER
            + Icons.SINGLE_H_ROAD * self.dimensions[1]
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
            for i in range(length):
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
                if self.data[row_st][col_st] == Icons.EMPTY:
                    self.data[row_st][col_st] = Tile(
                        Icons.H_ROAD, (row_st, col_st), name
                    )
                elif list2d_get(self.data, row_st, col_st, None) == Icons.V_ROAD:
                    self.data[row_st][col_st] = Tile(
                        Icons.CROSS, (row_st, col_st), name
                    )
                col_st += 1
            self.streets["horiz"][row_st] = name

    def add_buildings(self, num_buildings):
        eligible_spots = []
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if self.data[row][col] == Icons.EMPTY:
                    neighbors = self.get_neighbors(row, col)
                    if len(neighbors) == 1:
                        is_even = False
                        if (
                            neighbors[0].grid_loc[0] > row
                            or neighbors[0].grid_loc[1] > col
                        ):
                            is_even = True
                        if neighbors[0].icon == Icons.H_ROAD:
                            num = col * 2 if is_even else col * 2 + 1
                        else:
                            num = row * 2 if is_even else row * 2 + 1
                        name = f"{num} {neighbors[0].name}"
                        eligible_spots.append((row, col, name))

        buildings = list(Buildings)
        for spot in sample(eligible_spots, num_buildings):

            building = Tile(choice(buildings), (spot[0], spot[1]), spot[2])
            location = Location(
                spot[2], occupied=False, name="HOUSETYPE", floors="FLOORS"
            )
            self.buildings.append(location)
            self.data[spot[0]][spot[1]] = building

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
        if list2d_get(self.data, row - 1, col, Icons.EMPTY) != Icons.EMPTY:
            neighbors.append(self.data[row - 1][col])
        if list2d_get(self.data, row + 1, col, Icons.EMPTY) != Icons.EMPTY:
            neighbors.append(self.data[row + 1][col])
        if list2d_get(self.data, row, col - 1, Icons.EMPTY) != Icons.EMPTY:
            neighbors.append(self.data[row][col - 1])
        if list2d_get(self.data, row, col + 1, Icons.EMPTY) != Icons.EMPTY:
            neighbors.append(self.data[row][col + 1])
        return neighbors

    def sort_key(self, tile):
        # Split the name into parts
        parts = tile.address.split(" ", 1)  # Split into number and street name
        number = int(parts[0])  # First part is the number, convert to int
        street = parts[1]  # Second part is the street name
        return (street, number)

    def draw_map(self):
        print()
        print("The Map".center(self.dimensions[1]))
        print(self.top_border_row)
        for row_num, row in enumerate(self.data):
            char = Icons.SINGLE_V_ROAD
            if row_num in self.streets["horiz"]:
                char = self.streets["horiz"][row_num][0]
            print(char, end="")
            for col_num, col in enumerate(row):
                if [row_num, col_num] == self.current_location:
                    print(colored("⭑", "red"), end="")
                elif (
                    distance_points(self.current_location, (row_num, col_num))
                    > VIEW_DISTANCE
                ):
                    print("░", end="")
                else:
                    if isinstance(col, Tile):
                        print(col.icon, end="")
                    else:
                        print(col, end="")

            print(Icons.SINGLE_V_ROAD)
        print(self.bottom_border_row)

        # for loc in self.streets["vert"]:
        #     print(self.streets["vert"][loc])
        # for loc in self.streets["horiz"]:
        #     print(self.streets["horiz"][loc])

        for loc in sorted(
            self.buildings,
            key=self.sort_key,
        ):
            print(loc)
        # print(self.buildings)


street_map = Map()

street_map.add_road(False, 4, 1, 84)
street_map.add_road(False, 8, 25, 40)
street_map.add_road(True, 3, 2, 8)
street_map.add_road(False, 9, 5, 30)
street_map.add_road(True, 1, 28, 20)

street_map.add_buildings(40)
street_map.draw_map()
input()
street_map.move("RIGHT")
street_map.draw_map()
input()
street_map.move("RIGHT")
street_map.draw_map()
