from random import randint

from dataclasses import dataclass, field
from trait import Trait
from utility import create_table
from inventory import Inventory

INVENTORY_SIZE = 50


@dataclass
class Party:
    energy: Trait = Trait("Energy", 100, 100, 0)
    attitude: Trait = Trait("Attitude", 100, 100, 5)
    consumables: int = 50
    consumables_needed: int = 10
    supplies: int = 50
    settled: None = None
    scouted: list = field(default_factory=lambda: [])
    scavenged: list = field(default_factory=lambda: [])
    inventory = Inventory(INVENTORY_SIZE)

    @staticmethod
    def easy():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            consumables=50,
            consumables_needed=10,
            supplies=50,
            settled=None,
        )

    @staticmethod
    def average():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            consumables=50,
            consumables_needed=12,
            supplies=50,
            settled=None,
            scouted=[],
            scavenged=[],
            inventory=Inventory(INVENTORY_SIZE),
        )

    @staticmethod
    def hard():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            consumables=50,
            consumables_needed=15,
            supplies=50,
            settled=None,
            scouted=[],
            scavenged=[],
            inventory=Inventory(INVENTORY_SIZE),
        )

    @staticmethod
    def random():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            consumables=50,
            consumables_needed=randint(0, 50),
            supplies=randint(0, 50),
            settled=None,
            scouted=[],
            scavenged=[],
            inventory=Inventory(INVENTORY_SIZE),
        )

    @property
    def days_of_food(self):
        return self.consumables // self.consumables_needed

    # @property
    # def skills(self):
    #     return [
    #         self.negotiate_skill,
    #         self.threaten_skill,
    #         self.steal_skill,
    #         self.scout_skill,
    #         self.scavenge_skill,
    #         self.build_skill,
    #     ]

    def display_scouted_locations(self):
        if not self.scouted:
            print("No locations scouted")
            return
        table = [["#", "Location"]]
        table.extend([num, loc] for num, loc in enumerate(self.scouted, 1))
        print(create_table(table, header=True))

    def display_unoccupied_locations(self):
        unoccupied = [loc for loc in self.scouted if not loc.occupied]
        if not unoccupied:
            print("No unoccupied locations scouted")
            return
        for num, loc in enumerate(unoccupied, 1):
            print(f"{num}) {loc}")
        return unoccupied

    def display_occupied_locations(self):
        occupied = [loc for loc in self.scouted if loc.occupied]
        if not occupied:
            print("No occupied locations scouted")
            return
        for num, loc in enumerate(occupied, 1):
            print(f"{num}) {loc}")
        return occupied

    def settle_location(self, location):
        self.settled = location
        self.consumables += location.consumables
        print(f"Gained {location.consumables} consumables")
        self.supplies += location.supplies
        print(f"Gained {location.supplies} supplies")
        self.scouted.remove(location)

    def abandon_location(self):
        self.settled = None

    def travel(self, days_to_travel):
        # print(f"{days_to_travel} days will pass on your journey.")
        self.scouted = []
        self.scavenged = []

    def daily_energy_adjust(self, rest_amount):
        msg = ""
        if self.consumables >= self.consumables_needed:
            self.consumables -= self.consumables_needed
            msg += f"{self.consumables_needed} consumables eaten. "
        else:
            diff = self.consumables_needed - self.consumables
            self.consumables = 0
            # rest_amount -= diff
            self.energy.adjust_amount(-diff)
            msg += f"Not enough food, {diff} energy lost. "

        if self.settled:
            gain = int(self.settled.comfort.value / 10)
            rest_amount += gain
            self.energy.adjust_amount(rest_amount)
            msg += f"Settled, {gain} energy gained. "
        else:
            msg += "Unsettled, no energy gained. "

        return msg

    def display_full_stats(self):
        self.display_party_stats()
        # self.display_party_skills()
        if self.settled:
            self.display_settled_stats()
        else:
            print("Party is currently unsettled.")
        print(f"Party has scouted {len(self.scouted)} locations.")
        if self.scouted:
            self.display_scouted_locations()

    def display_party_stats(self):
        print(self.energy)
        # print(self.attitude)
        print("Consumables:", self.consumables, f"({self.days_of_food} days)")
        print("Supplies:", self.supplies)
        print(self.inventory.summary())

    # def display_party_skills(self, numberize=False):
    #     # skills = ["a", "b", "c"]
    #     for num, skill in enumerate(self.skills):
    #         if numberize:
    #             print(f"{num}) {skill}")
    #         else:
    #             print(skill)

    def display_settled_stats(self):
        print(f"Party is settled at {self.settled.address}")
        print("\t", self.settled.protection)
        print("\t", self.settled.comfort)
