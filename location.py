from dataclasses import dataclass
from random import choice, randint
from trait import Trait

PROTECTION_DECAY_AMOUNT = 1
COMFORT_DECAY_AMOUNT = 1

DESCRIPTIONS = {
    "protection": {
        0: "no doors or windows, open structure with exposed interior.",
        10: "basic door frame with no locks, uncovered windows, no visible barriers.",
        20: "simple wood doors, single-pane windows with no bars or reinforcement, minimal fencing.",
        30: "standard doors with deadbolts, standard single-pane glass, low garden fence.",
        40: "thicker doors, double-pane windows, visible basic locks, low hedges or walls.",
        50: "heavy wood or metal doors, impact-resistant windows, moderate-height fence or wall.",
        60: "steel-framed doors, shatter-resistant windows, taller fence or stone wall.",
        70: "reinforced steel doors, laminated glass, security cameras or motion lights, tall fence with restricted view.",
        80: "steel doors with bar locks, bulletproof glass, high walls, multiple cameras, visible alarm system.",
        90: "thick steel-reinforced walls, multi-layered windows, surveillance towers, visible guard equipment.",
        100: "armored doors, blast-resistant windows, high perimeter walls with barbed wire, extensive surveillance, visible entry restrictions (gates, guards).",
    }
}


@dataclass
class Location:
    address: str
    occupied: bool = False
    name: str = "Townhouse"
    floors: int = 1
    protection: Trait = Trait("Protection", 50, 100, PROTECTION_DECAY_AMOUNT)
    comfort: Trait = Trait("Comfort", 70, 100, COMFORT_DECAY_AMOUNT)
    consumables: int = 0
    supplies: int = 0

    @staticmethod
    def random_location():
        return Location(
            address=f"{randint(1, 200)} Fake St.",
            occupied=choice([True, False]),
            name="house",
            floors=randint(1, 4),
            protection=Trait(
                "Protection", randint(0, 100), 100, PROTECTION_DECAY_AMOUNT
            ),
            comfort=Trait("Comfort", randint(0, 100), 100, COMFORT_DECAY_AMOUNT),
            consumables=randint(0, 100),
            supplies=randint(0, 100),
        )

    def describe(self):
        msg = f"{self.address}: a {'single' if self.floors == 1 else self.floors} story townhouse. "
        msg += f"It looks {'un' if not self.occupied else ''}occupied. "
        msg += f"It appears to have {DESCRIPTIONS['protection'][round(self.protection.value, -1)]} "
        return msg

    # def describe_exterior(self):
    #     msg = "An "
    #     if not self.occupied:
    #         msg += "un"
    #     msg += f"occupied {self.name}. "
    #     # msg += f"It appears {protection_words[int(self.protection//BUCKET_SIZE)]}. "
    #     # msg += f"Looks like a {comfort_words[int(self.comfort//BUCKET_SIZE)]} place to stay "
    #     return msg

    # def describe_interior(self):
    #     msg = "It looks "
    #     if not self.occupied:
    #         msg += "un"
    #     msg += "occupied. "
    #     msg += "We found a lot of junk."

    def __str__(self):
        return self.describe()
