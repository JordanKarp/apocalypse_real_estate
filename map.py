from random import choice


def create_road(name):
    string = ""
    for letter in name:
        string += f"| {letter} |\n"

    return string


print(create_road("MAIN ST"))


map_string = """
_R_.......
_R_.......
_R_...._R_
_R_...._R_
_R_...._R_
_R_...._R_
_R_...._R_
RRRRRRRRRRR
_R_...._R_
_R_...._R_
_R_...._R_
"""


def create_road():
    road_names = ["MAIN ST", "FIRST ST", "BEACON AVE"]

    return ""


def gen_map_string():
    string = ""
    num_roads = 2
    vert = True
    density = 0.4
    for _ in range(num_roads):
        create_road()
