from enum import Enum


class Menu(str, Enum):
    SHOW_SCOUTED = "Show currently scouted homes"
    SHOW_PARTY = "Show current party stats"
    NOTHING = "Do nothing (1 day)"
    IMPROVE = "Improve Party (1 day)"
    TRAVEL = "Travel to new area (3 days)"
    SCOUT = "Scout nearby homes (10 Energy)"
    SETTLE = "Settle an unoccupied home (1 day)"
    SCAVENGE = "Scavenge a unoccupied home (1 day)"
    NEGOTIATE = "Negotiate with another party for supplies (1 day)"
    THREATEN = "Threaten with another party for supplies (1 day)"
    STEAL = "Steal supplies from  another party  (1 day)"
    IMPROVE_COMFORT = "Improve home comfort (1 day)"
    IMPROVE_PROTECTION = "Improve home protection (1 day)"
    ABANDON = "Abandon current home"
    QUIT = "Give up (Quit)"

    def __str__(self) -> str:
        return str.__str__(self)
