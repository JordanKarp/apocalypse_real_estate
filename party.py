from dataclasses import dataclass, field
from trait import Trait


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
    charisma_skill: Trait = Trait("Charisma Skill", 50, 100, 0)
    intimidation_skill: Trait = Trait("Intimidation Skill", 50, 100, 0)
    camouflage_skill: Trait = Trait("Camouflage Skill", 50, 100, 0)
    scout_skill: Trait = Trait("Scout Skill", 50, 100, 0)
    scavenge_skill: Trait = Trait("Scavenge Skill", 50, 100, 0)
    building_skill: Trait = Trait("Building Skill", 50, 100, 0)

    @property
    def skills(self):
        return [
            self.charisma_skill,
            self.intimidation_skill,
            self.camouflage_skill,
            self.scout_skill,
            self.scavenge_skill,
            self.building_skill,
        ]

    def display_scouted_locations(self):
        if not self.scouted:
            print("No locations scouted")
            return
        for num, loc in enumerate(self.scouted, 1):
            print(f"{num}) {loc}")

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

    def daily_energy_adjust(self, rest_amount):
        if self.consumables <= 0:
            amt = rest_amount - self.consumables_needed
            self.energy.adjust_amount(rest_amount - self.consumables_needed)
            print(f"No food, {amt} energy lost")
        elif self.consumables < self.consumables_needed:
            amt = rest_amount - (self.consumables_needed - self.consumables)
            self.energy.adjust_amount(amt)
            self.consumables = 0
            if amt > 0:
                print(f"Limited food, {amt} energy gained")
            else:
                print(f"Limited food, {amt} energy lost")

        else:
            self.consumables -= self.consumables_needed
            self.energy.adjust_amount(rest_amount)
            print(f"{rest_amount} energy gained")

    def display_full_stats(self):
        self.display_party_stats()
        if self.settled:
            self.display_settled_stats()
        else:
            print("Party is currently unsettled.")
        self.display_party_skills()
        print(f"Party has scouted {len(self.scouted)} locations.")
        if self.scouted:
            self.display_scouted_locations()

    def display_party_stats(self):
        print(self.energy)
        print(self.attitude)
        print("Consumables:", self.consumables)
        print("Supplies:", self.supplies)

    def display_party_skills(self, enumerate=False):
        if enumerate:
            print("1)", self.charisma_skill)
            print("2)", self.intimidation_skill)
            print("3)", self.camouflage_skill)
            print("4)", self.scout_skill)
            print("5)", self.scavenge_skill)
            print("6)", self.building_skill)
        else:
            print(self.charisma_skill)
            print(self.intimidation_skill)
            print(self.camouflage_skill)
            print(self.scout_skill)
            print(self.scavenge_skill)
            print(self.building_skill)

    def display_settled_stats(self):
        print(f"Party is settled at {self.settled.address}")
        print("\t", self.settled.protection)
        print("\t", self.settled.comfort)
