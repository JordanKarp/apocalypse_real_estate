from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class MainMenu(StrEnum):
    NEW = "Play new game"
    LOAD = "Load a game"
    OPTIONS = "Options"
    HELP = "Help"
    HIGH_SCORES = "High Scores"
    QUIT = "Quit"


class ApocalypseMenu(StrEnum):
    PANDEMIC = "Pandemic"
    HURRICANE = "Hurricane"
    WINTER = "Impact Winter"


class PartyMenu(StrEnum):
    EASY = "Easy difficulty party"
    AVERAGE = "Average difficulty party"
    HARD = "Hard difficulty party"
    RANDOM = "Random"
    CUSTOM = "Custom party"


class OptionsMenu(StrEnum):
    DEFAULT_NAME = "Default High Score Name"
    BACK = "Back to Main Menu"


class GameMenu(StrEnum):
    SHOW_SCOUTED = "Show currently scouted homes"
    SHOW_PARTY = "Show current party stats"
    NOTHING = "Do nothing"
    IMPROVE = "Improve Party"
    TRAVEL = "Travel to new area"
    SCOUT = "Scout nearby homes"
    SETTLE = "Settle an unoccupied home"
    SCAVENGE = "Scavenge a unoccupied home"
    NEGOTIATE = "Negotiate with another party for supplies"
    THREATEN = "Threaten with another party for supplies"
    STEAL = "Steal supplies from  another party "
    INCREASE_COMFORT = "Improve home comfort"
    INCREASE_PROTECTION = "Improve home protection"
    ABANDON = "Abandon current home"
    QUIT = "Give up (Quit)"
