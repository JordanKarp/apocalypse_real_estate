from random import randint

from dataclasses import dataclass, field
from trait import Trait
from utility import create_table


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
    negotiate_skill: Trait = Trait("Negotiate Skill", 50, 100, 0)
    threaten_skill: Trait = Trait("Threaten Skill", 50, 100, 0)
    steal_skill: Trait = Trait("Steal Skill", 50, 100, 0)
    scout_skill: Trait = Trait("Scout Skill", 50, 100, 0)
    scavenge_skill: Trait = Trait("Scavenge Skill", 50, 100, 0)
    build_skill: Trait = Trait("Building Skill", 50, 100, 0)

    @staticmethod
    def easy():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            attitude=Trait("Attitude", 100, 100, 5),
            consumables=50,
            consumables_needed=10,
            supplies=50,
            settled=None,
            scouted=[],
            scavenged=[],
            negotiate_skill=Trait("Negotiate Skill", 75, 100, 0),
            threaten_skill=Trait("Threaten Skill", 75, 100, 0),
            steal_skill=Trait("Steal Skill", 75, 100, 0),
            scout_skill=Trait("Scout Skill", 75, 100, 0),
            scavenge_skill=Trait("Scavenge Skill", 75, 100, 0),
            build_skill=Trait("Building Skill", 75, 100, 0),
        )

    @staticmethod
    def average():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            attitude=Trait("Attitude", 100, 100, 5),
            consumables=50,
            consumables_needed=12,
            supplies=50,
            settled=None,
            scouted=[],
            scavenged=[],
            negotiate_skill=Trait("Negotiate Skill", 50, 100, 0),
            threaten_skill=Trait("Threaten Skill", 50, 100, 0),
            steal_skill=Trait("Steal Skill", 50, 100, 0),
            scout_skill=Trait("Scout Skill", 50, 100, 0),
            scavenge_skill=Trait("Scavenge Skill", 50, 100, 0),
            build_skill=Trait("Building Skill", 50, 100, 0),
        )

    @staticmethod
    def hard():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            attitude=Trait("Attitude", 100, 100, 5),
            consumables=50,
            consumables_needed=15,
            supplies=50,
            settled=None,
            scouted=[],
            scavenged=[],
            negotiate_skill=Trait("Negotiate Skill", 25, 100, 0),
            threaten_skill=Trait("Threaten Skill", 25, 100, 0),
            steal_skill=Trait("Steal Skill", 25, 100, 0),
            scout_skill=Trait("Scout Skill", 25, 100, 0),
            scavenge_skill=Trait("Scavenge Skill", 25, 100, 0),
            build_skill=Trait("Building Skill", 25, 100, 0),
        )

    @staticmethod
    def random():
        return Party(
            energy=Trait("Energy", 100, 100, 0),
            attitude=Trait("Attitude", 100, 100, 5),
            consumables=50,
            consumables_needed=randint(0, 50),
            supplies=randint(0, 50),
            settled=None,
            scouted=[],
            scavenged=[],
            negotiate_skill=Trait("Negotiate Skill", randint(0, 100), 100, 0),
            threaten_skill=Trait("Threaten Skill", randint(0, 100), 100, 0),
            steal_skill=Trait("Steal Skill", randint(0, 100), 100, 0),
            scout_skill=Trait("Scout Skill", randint(0, 100), 100, 0),
            scavenge_skill=Trait("Scavenge Skill", randint(0, 100), 100, 0),
            build_skill=Trait("Building Skill", randint(0, 100), 100, 0),
        )

    @property
    def days_of_food(self):
        return self.consumables // self.consumables_needed

    @property
    def skills(self):
        return [
            self.negotiate_skill,
            self.threaten_skill,
            self.steal_skill,
            self.scout_skill,
            self.scavenge_skill,
            self.build_skill,
        ]

    def display_scouted_locations(self):
        if not self.scouted:
            print("No locations scouted")
            return
        table = [["#", "Location"]]
        for num, loc in enumerate(self.scouted, 1):
            table.append([num, loc])
        print(create_table(table, True))
        # for num, loc in enumerate(self.scouted, 1):
        #     print(f"{num}) {loc}")

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
        self.supplies += location.supplies
        self.scouted.remove(location)

    def abandon_location(self):
        self.settled = None

    def daily_energy_adjust(self, rest_amount):
        if self.consumables >= self.consumables_needed:
            self.consumables -= self.consumables_needed
            print(f"{self.consumables_needed} consumables eaten")
        else:
            diff = self.consumables_needed - self.consumables
            self.consumables = 0
            # rest_amount -= diff
            self.energy.adjust_amount(-diff)
            print(f"Not enough food, {diff} energy lost.")

        if self.settled:
            gain = int(self.settled.comfort.value / 10)
            rest_amount += gain
            self.energy.adjust_amount(rest_amount)
            print(f"Settled, {gain} energy gained.")
        else:
            print("Unsettled, no energy gained.")

        # if self.consumables <= 0:
        #     amt = rest_amount - self.consumables_needed
        #     self.energy.adjust_amount(amt)
        #     print(f"No food, {amt} energy lost")
        # elif self.consumables < self.consumables_needed:
        #     amt = rest_amount - (self.consumables_needed - self.consumables)
        #     self.energy.adjust_amount(amt)
        #     self.consumables = 0
        #     if amt > 0:
        #         print(f"Limited food, {amt} energy gained")
        #     else:
        #         print(f"Limited food, {amt} energy lost")

        # else:
        #     self.consumables -= self.consumables_needed
        #     self.energy.adjust_amount(rest_amount)
        #     if rest_amount > 0:
        #         print(f"{rest_amount} energy gained")
        #     else:

        #         print(f"{-rest_amount} energy lost")

    def display_full_stats(self):
        self.display_party_stats()
        self.display_party_skills()
        if self.settled:
            self.display_settled_stats()
        else:
            print("Party is currently unsettled.")
        print(f"Party has scouted {len(self.scouted)} locations.")
        if self.scouted:
            self.display_scouted_locations()

    def display_party_stats(self):
        print(self.energy)
        print(self.attitude)
        print("Consumables:", self.consumables, f"({self.days_of_food} days)")
        print("Supplies:", self.supplies)

    def display_party_skills(self, enumerate=False):
        if enumerate:
            print("1)", self.negotiate_skill)
            print("2)", self.threaten_skill)
            print("3)", self.steal_skill)
            print("4)", self.scout_skill)
            print("5)", self.scavenge_skill)
            print("6)", self.build_skill)
        else:
            print(self.negotiate_skill)
            print(self.threaten_skill)
            print(self.steal_skill)
            print(self.scout_skill)
            print(self.scavenge_skill)
            print(self.build_skill)

    def display_settled_stats(self):
        print(f"Party is settled at {self.settled.address}")
        print("\t", self.settled.protection)
        print("\t", self.settled.comfort)
