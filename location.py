from dataclasses import dataclass
from random import random, randint


@dataclass
class Location:
    occupied: bool = False
    name: str = "House"
    protected: float = 0.0
    hidden_site: float = 0.0
    concealed: float = 0.0
    accessible: float = 0.0
    comfortable: float = 0.0
    waterproof: float = 0.0
    fireproof: float = 0.0

    observable_range: int = 0
    consumables: int = 0
    supplies: int = 0

    @staticmethod
    def random():
        return Location(
            occupied=False,
            name="house",
            protected=round(random(), 2),
            hidden_site=round(random(), 2),
            concealed=round(random(), 2),
            accessible=round(random(), 2),
            comfortable=round(random(), 2),
            waterproof=round(random(), 2),
            fireproof=round(random(), 2),
            observable_range=randint(0, 100),
            consumables=randint(0, 100),
            supplies=randint(0, 100),
        )

    def describe(self):
        BUCKET_SIZE = 0.2
        protection_words = [
            "Vulnerable",
            "Fragile",
            "Moderately Protected",
            "Reinforced and Sturdy",
            "Impenetrable",
        ]
        hidden_words = [
            "In plain sight",
            "Visible",
            "Obscured",
            "Camouflaged",
            "Hidden",
        ]

        accessible_words = [
            "Inaccessible",
            "Hard to Access",
            "Challenging to get to",
            "Accessible",
            "Easily Accessible",
        ]
        comfort_words = [
            "Unbearable",
            "Uncomfortable",
            "Tolerable",
            "Cozy",
            "Luxurious",
        ]
        waterproof_words = [
            "Not waterproof",
            "Water-resistant",
            "Water-repellent",
            "Waterproof",
            "Submersible",
        ]
        fireproof_words = [
            "Not fireproof",
            "Fire-resistant",
            "Fire-retardant",
            "Fireproof",
            "Fire-safe",
        ]

        observable_range = [
            "Close range",
            "Short distance",
            "Moderate distance",
            "Long distance",
            "Far vantage",
        ]
        provisioned_scale = [
            "Bare",
            "Sparsely stocked",
            "Adequately stocked",
            "Well stocked",
            "Fully stocked",
        ]

        msg = "An "
        if not self.occupied:
            msg += "un"
        msg += f"occupied {self.name}. "
        msg += f"It appears {protection_words[int(self.protected//BUCKET_SIZE)]}. "
        msg += f"It is {hidden_words[int(self.hidden_site//BUCKET_SIZE)]} "
        msg += f"and {accessible_words[int(self.accessible//BUCKET_SIZE)]} from the main road."
        msg += f"Looks like a {comfort_words[int(self.comfortable//BUCKET_SIZE)]} place to stay "
        msg += f"thats {waterproof_words[int(self.waterproof//BUCKET_SIZE)]}, {fireproof_words[int(self.fireproof//BUCKET_SIZE)]}, and {provisioned_scale[int(self.consumables//(BUCKET_SIZE* 100))]}."
        return msg

    def __str__(self):
        return self.describe()
