from enum import Enum
from dataclasses import dataclass
from typing import Union


class Icons(str, Enum):
    SINGLE_V_ROAD = "│"
    SINGLE_H_ROAD = "─"
    SINGLE_TR_CORNER = "┐"
    SINGLE_TL_CORNER = "┌"
    SINGLE_BR_CORNER = "┘"
    SINGLE_BL_CORNER = "└"
    SINGLE_T_DOWN = "┬"
    SINGLE_T_UP = "┴"
    SINGLE_T_LEFT = "┤"
    SINGLE_T_RIGHT = "├"
    SINGLE_CROSS = "┼"
    V_ROAD = "║"
    H_ROAD = "═"
    TR_CORNER = "╗"
    TL_CORNER = "╔"
    BR_CORNER = "╝"
    BL_CORNER = "╚"
    T_DOWN = "╦"
    T_UP = "╩"
    T_LEFT = "╣"
    T_RIGHT = "╠"
    CROSS = "╬"
    EMPTY = " "
    BUILDING = "█"

    def __str__(self) -> str:
        return str.__str__(self)


class Buildings(str, Enum):
    LOWER_1_2 = "▄"
    LOWER_5_8 = "▅"
    LOWER_3_4 = "▆"
    LOWER_7_8 = "▇"
    FULL = "█"
    # LIGHT_SHADE = "░"
    MED_SHADE = "▒"
    DARK_SHADE = "▓"
    SQUARE_FULL = "■"
    SQUARE_EMPTY = "□"
    SQUARE_EMPTY_FULL = "▣"
    SQUARE_EMPTY_ROUND = "▢"
    SQUARE_HORIZ = "▤"
    SQUARE_VERT = "▥"
    SQUARE_CROSS = "▦"
    SQUARE_DIAG_LR = "▧"
    SQUARE_DIAG_RL = "▨"
    SQUARE_DIAG = "▩"
    SM_SQUARE = "▪"
    SM_SQUARE_EMPTY = "▫"
    TRIANGLE = "▲"
    # LEFT_HALF = "▌"
    # RIGHT_HALF = "▐"
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


@dataclass
class Tile:
    icon: Icons = Icons.EMPTY
    grid_loc: Union[int, int] = (0, 0)
    name: str = "MAIN"

    def __eq__(self, other):
        if isinstance(other, Icons):
            return self.icon == other
        elif not isinstance(other, Tile):
            return False
        return self.icon == other.icon and self.name == other.name

    # def __repr__(self) -> str:
    #     return self.icon


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
