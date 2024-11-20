from random import choice, randint
from enum import Enum
from utility import list2d_get, colored

MIN_ROAD_LENGTH = 3
ROAD_NAMES = [
    "MAIN STREET",
    "OAK AVENUE",
    "PINE ROAD",
    "MAPLE LANE",
    "CEDAR DRIVE",
    "ELM STREET",
    "WILLOW WAY",
    "ASH COURT",
    "BIRCH BOULEVARD",
    "SPRUCE TRAIL",
    "CHESTNUT PLACE",
    "HICKORY ROAD",
    "CYPRESS CIRCLE",
    "BEECH AVENUE",
    "LOCUST LANE",
    "MAGNOLIA STREET",
    "DOGWOOD DRIVE",
    "REDWOOD ROAD",
    "PALM WAY",
    "HOLLY COURT",
    "ALDER ROAD",
    "JUNIPER BOULEVARD",
    "SEQUOIA TRAIL",
    "POPLAR PLACE",
    "FIR STREET",
]


class Buildings(str, Enum):
    FULL = "█"
    LOWER_HALF = "▄"
    LOWER_34 = "▆"
    LEFT_HALF = "▌"
    RIGHT_HALF = "▐"
    LL = "▖"
    UL = "▘"
    LR = "▗"
    UR = "▝"
    # QLL = "▙"
    # QUL = "▛"
    # QLR = "▟"
    # QUR = "▜"

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Tiles(str, Enum):
    V_ROAD = "│"
    H_ROAD = "─"
    TR_CORNER = "┐"
    TL_CORNER = "┌"
    BR_CORNER = "┘"
    BL_CORNER = "└"

    EMPTY = " "
    BUILDING = "█"

    def __str__(self) -> str:
        return str.__str__(self)


class Map:
    def __init__(self, dimensions=(15, 45)):
        self.dimensions = dimensions
        self.streets = []
        self.current_location = (4, 27)
        self.data = [[" " for _ in range(dimensions[1])] for _ in range(dimensions[0])]

    @property
    def top_row(self):
        return Tiles.TL_CORNER + (Tiles.H_ROAD * self.dimensions[1] + Tiles.TR_CORNER)

    @property
    def bottom_row(self):
        return Tiles.BL_CORNER + (Tiles.H_ROAD * self.dimensions[1] + Tiles.BR_CORNER)

    def add_random_road(self, num=1):
        name = choice(ROAD_NAMES)
        is_vert = choice([True, False])
        row_st = randint(1, self.dimensions[0] - 1)
        col_st = randint(1, self.dimensions[1] - 1)
        if is_vert and self.dimensions[1] - col_st >= MIN_ROAD_LENGTH:
            length = randint(MIN_ROAD_LENGTH, self.dimensions[1] - col_st)
        elif not is_vert and self.dimensions[0] - row_st >= MIN_ROAD_LENGTH:
            length = randint(MIN_ROAD_LENGTH, self.dimensions[0] - row_st)
        else:
            length = 0

        # print(is_vert, row_st, col_st, length)
        self.add_road(name, is_vert, row_st, col_st, length)

    def add_road(self, name, is_vert, row_st, col_st, length):
        if is_vert:
            rd = self.add_vertical_road(name, row_st, col_st, length)
        else:
            rd = self.add_horizontal_road(name, row_st, col_st, length)
        self.streets.append(rd)

    def add_vertical_road(self, name, row_st, col_st, length):
        # name = name.center(length).replace(" ", "│")
        name = "│" * length

        name_id = 0
        if length:
            for _ in range(length):
                if list2d_get(self.data, row_st, col_st, None) == Tiles.EMPTY:
                    self.data[row_st][col_st] = name[name_id]
                elif list2d_get(self.data, row_st, col_st, None) == Tiles.H_ROAD:
                    self.data[row_st][col_st] = "┼"

                row_st += 1
                name_id += 1

    def add_horizontal_road(self, name, row_st, col_st, length):
        # name = name.center(length).replace(" ", "─")
        name = "─" * length
        name_id = 0
        if length:
            for _ in range(length):
                if self.data[row_st][col_st] == Tiles.EMPTY:
                    self.data[row_st][col_st] = name[name_id]
                elif list2d_get(self.data, row_st, col_st, None) == Tiles.V_ROAD:
                    self.data[row_st][col_st] = "┼"
                col_st += 1
                name_id += 1

    def add_buildings(self, num_buildings):
        eligible_spots = []
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if self.data[row][col] == Tiles.EMPTY:
                    neighbors = self.get_neighbors(row, col)
                    if neighbors == 1:
                        eligible_spots.append((row, col))

        for _ in range(num_buildings):
            spot = choice(eligible_spots)
            # self.remove_neighbors(eligible_spots, spot)
            buildings = list(Buildings)
            scouted = choice([True, False])
            if scouted:
                self.data[spot[0]][spot[1]] = colored(choice(buildings), "green")
            else:
                self.data[spot[0]][spot[1]] = colored(choice(buildings), "yellow")

    def remove_neighbors(self, eligible_spots, spot):
        if (spot[0] - 1, spot[1]) in eligible_spots:
            eligible_spots.remove((spot[0] - 1, spot[1]))
        elif (spot[0] + 1, spot[1]) in eligible_spots:
            eligible_spots.remove((spot[0] + 1, spot[1]))
        elif (spot[0], spot[1] - 1) in eligible_spots:
            eligible_spots.remove((spot[0], spot[1] - 1))
        elif (spot[0], spot[1] + 1) in eligible_spots:
            eligible_spots.remove((spot[0], spot[1] + 1))

    def get_neighbors(self, row, col):
        neighbors = 0
        if list2d_get(self.data, row - 1, col, Tiles.EMPTY) != Tiles.EMPTY:
            neighbors += 1
        if list2d_get(self.data, row + 1, col, Tiles.EMPTY) != Tiles.EMPTY:
            neighbors += 1
        if list2d_get(self.data, row, col - 1, Tiles.EMPTY) != Tiles.EMPTY:
            neighbors += 1
        if list2d_get(self.data, row, col + 1, Tiles.EMPTY) != Tiles.EMPTY:
            neighbors += 1
        return neighbors

    def draw_map(self):
        print(self.top_row)
        for row_num, row in enumerate(self.data):
            print("│", end="")
            for col_num, col in enumerate(row):
                if (row_num, col_num) == self.current_location:
                    print(colored("*", "red"), end="")
                else:
                    print(col, end="")
            print("│")
        print(self.bottom_row)


street_map = Map()

street_map.add_road("Main", False, 4, 1, 44)
street_map.add_road("Second", False, 8, 25, 10)
street_map.add_road("Oak", True, 3, 2, 8)
street_map.add_road("Elm", False, 9, 5, 30)
street_map.add_road("Pine", True, 1, 28, 20)

street_map.add_buildings(40)
street_map.draw_map()
