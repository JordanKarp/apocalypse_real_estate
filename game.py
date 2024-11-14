from random import randint

from apocalypse import Apocalypse
from apocalypse_scenarios import ApocalypseScenarios
from location import Location
from menu_options import GameMenu
from party import Party
from utility import clear, colored, pick_option, create_table
from state import State


REST_ADD_AMOUNT = 5
SKILL_ADD_AMOUNT = 5
TRAVEL_DAYS = 3
SCOUT_COST = 5
IMPROVE_COST = 5
SETTLE_COST = 5
SCAVENGE_COST = 5
NEGOTIATE_COST = 5
THREATEN_COST = 5
ABANDON_COST = 5
STEAL_COST = 5
BUILD_COST = 5
DEFAULT_SCAV = 10
PROTECTION_ADD_AMOUNT = 5
COMFORT_ADD_AMOUNT = 5
NEGOTIATE_CHANCE = 0.75
MAX_SCOUT = 5
NUM_DEFENDING_CHANCES = 3
SUPPLIES_NEEDED_TO_BUILD = 10


class Game(State):
    def __init__(self):
        super().__init__()
        self.playing = True
        self.day_number = 1
        self.days_to_pass = 1
        self.apocalypse = None
        self.party = None
        self.locations = []

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent
        self.apocalypse = self.persist.get("apocalypse", "Pandemic")
        self.party = self.persist.get("party", Party())

    def print_header(self):
        print("-" * 5, f"Day {self.day_number} - {self.apocalypse.name}", "-" * 5)
        self.party.display_full_stats()
        print("-" * 28)

    def present_options(self):
        options = [
            # (GameMenu.SHOW_SCOUTED, None),
            # (GameMenu.SHOW_PARTY, None),
            (GameMenu.NOTHING, 0, 0),
            (GameMenu.SCOUT, int(SCOUT_COST * self.apocalypse.mult["scout_cost"]), 0),
            (
                GameMenu.IMPROVE,
                int(IMPROVE_COST * self.apocalypse.mult["improve_cost"]),
                0,
            ),
        ]

        if not self.party.settled:
            options.append(
                (
                    GameMenu.TRAVEL,
                    f"{int(TRAVEL_DAYS * self.apocalypse.mult['travel_cost'])} days",
                    0,
                )
            )

        if self.party.scouted:
            if any(not loc.occupied for loc in self.party.scouted):
                options.append(
                    (
                        GameMenu.SETTLE,
                        int(SETTLE_COST * self.apocalypse.mult["settle_cost"]),
                        SUPPLIES_NEEDED_TO_BUILD,
                    )
                )
                options.append(
                    (
                        GameMenu.SCAVENGE,
                        int(SCAVENGE_COST * self.apocalypse.mult["scavenge_cost"]),
                        0,
                    )
                )

            if any(loc.occupied for loc in self.party.scouted):
                options.append(
                    (
                        GameMenu.NEGOTIATE,
                        int(NEGOTIATE_COST * self.apocalypse.mult["negotiate_cost"]),
                        0,
                    )
                )
                options.append(
                    (
                        GameMenu.THREATEN,
                        int(THREATEN_COST * self.apocalypse.mult["threaten_cost"]),
                        0,
                    )
                )
                options.append(
                    (
                        GameMenu.STEAL,
                        int(STEAL_COST * self.apocalypse.mult["steal_cost"]),
                        0,
                    )
                )

        if self.party.settled:
            options.append(
                (
                    GameMenu.INCREASE_PROTECTION,
                    int(BUILD_COST * self.apocalypse.mult["build_protection_cost"]),
                    SUPPLIES_NEEDED_TO_BUILD,
                )
            )
            options.append(
                (
                    GameMenu.INCREASE_COMFORT,
                    int(BUILD_COST * self.apocalypse.mult["build_comfort_cost"]),
                    SUPPLIES_NEEDED_TO_BUILD,
                )
            )
            options.append(
                (
                    GameMenu.ABANDON,
                    int(ABANDON_COST * self.apocalypse.mult["abandon_cost"]),
                    0,
                )
            )

        options.append((GameMenu.QUIT, None, None))

        table = [["#", "Description", "Energy", "Supplies"]]
        for num, (opt, cost, sup) in enumerate(options, 1):
            if isinstance(cost, int):
                table.append([f"{num}.", opt, cost, sup])
                # print(f"{num}. ({cost} energy) {opt}")
            elif isinstance(cost, str):
                table.append([f"{num}.", opt, cost, sup])
                # print(f"{num}. ({cost}) {opt}")
            else:
                table.append([f"{num}.", opt, "", ""])
                # print(f"{num}. {opt}")

        print(create_table(table, True))
        return [opt for opt, _, _ in options]

    def implement(self, choice_str):
        # DISPLAY OPTIONS
        if choice_str == GameMenu.SHOW_SCOUTED:
            self.party.display_scouted_locations()
            input("Press enter to return to menu.")
            self.deciding_loop()

        elif choice_str == GameMenu.SHOW_PARTY:
            self.party.display_full_stats()
            input("Press enter to return to menu.")
            self.deciding_loop()

        elif choice_str == GameMenu.NOTHING:
            pass

        elif choice_str == GameMenu.IMPROVE:
            self.party.display_party_skills(enumerate=True)
            choice = pick_option(
                "Which skill would you like to improve?", self.party.skills
            )
            choice.adjust_amount(SKILL_ADD_AMOUNT)
            print(f"{choice.name} was improved by {SKILL_ADD_AMOUNT}")
            print(choice)

            amt = int(IMPROVE_COST * self.apocalypse.mult["improve_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy improving {choice.name}")

        elif choice_str == GameMenu.TRAVEL:
            self.days_to_pass = TRAVEL_DAYS * self.apocalypse.mult["travel_cost"]
            print(f"{self.days_to_pass} days pass on your journey.")

        elif choice_str == GameMenu.SCOUT:
            # TODO make better than adding 1-3 random locations
            new_locs = int(MAX_SCOUT * self.party.scout_skill.percent)
            locs = []
            for _ in range(new_locs):
                location = Location.random_location()
                self.party.scouted.append(location)
                locs.append(location)
            print(f"{new_locs} new location(s) found.")
            for loc in locs:
                print("\t-", loc)

            amt = int(SCOUT_COST * self.apocalypse.mult["scout_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy scouting")

        elif choice_str == GameMenu.SETTLE:
            locs = self.party.display_unoccupied_locations()
            choice = pick_option("Which location to settle?", locs)
            self.party.settle_location(choice)
            print(choice.address, "has been settled.")

            amt = int(SETTLE_COST * self.apocalypse.mult["settle_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy settling new location.")

        elif choice_str == GameMenu.SCAVENGE:

            # Pick place
            locs = self.party.display_unoccupied_locations()
            choice = pick_option("Which location to scavage?", locs)
            # Determine amount to scavenge

            # ! FIX TO BE PERCENT CHANCE
            amount_to_scav = int(DEFAULT_SCAV * self.party.scavenge_skill.percent)
            # Split between food and supplys
            consume = randint(1, amount_to_scav)
            supply = amount_to_scav - consume
            # gain amount, or as much as they have of each type
            if choice.supplies >= supply:
                amt = supply
            else:
                amt = choice.supplies
            self.party.supplies += amt
            print(f"Gained {amt} supplies.")

            if choice.consumables >= consume:
                amt = consume
            else:
                amt = choice.supplies
            self.party.consumables += amt
            print(f"Gained {amt} consumables.")

            # Remove rest of materials
            choice.consumables = 0
            choice.supplies = 0
            # Fix lists
            self.party.scouted.remove(choice)
            self.party.scavenged.append(choice)

            amt = SCAVENGE_COST * self.apocalypse.mult["scavenge_cost"]
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy scavenging")

        elif choice_str == GameMenu.NEGOTIATE:
            # Pick place
            locs = self.party.display_occupied_locations()
            choice = pick_option("With which location do you want to negotiate?", locs)
            vals = []
            for _ in range(NUM_DEFENDING_CHANCES):
                vals.append(randint(1, choice.protection.value))
            defending = max(vals)
            attacking = randint(0, self.party.negotiate_skill.value)
            if defending < attacking:
                print("Success!")
                cons = int(choice.consumables / 2)
                sups = int(choice.supplies / 2)
                choice.consumables -= cons
                choice.supplies -= sups
                self.party.consumables += cons
                self.party.supplies += sups
                print(f"Got half their consumables ({cons}) and supplies ({sups})")
            else:
                print("Fail. Negotiations unsuccessful")

            amt = int(NEGOTIATE_COST * self.apocalypse.mult["negotiate_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy negotiating")

        elif choice_str == GameMenu.THREATEN:
            # Pick place
            locs = self.party.display_occupied_locations()
            choice = pick_option("Which location do you want to threaten?", locs)
            vals = []
            for _ in range(NUM_DEFENDING_CHANCES):
                vals.append(randint(1, choice.protection.value))
            defending = max(vals)
            attacking = randint(0, self.party.threaten_skill.value)
            if defending < attacking:
                print("Success!")
                cons = int(choice.consumables / 2)
                sups = int(choice.supplies / 2)
                choice.consumables -= cons
                choice.supplies -= sups
                self.party.consumables += cons
                self.party.supplies += sups
                print(f"Got half their consumables ({cons}) and supplies ({sups})")
            else:
                print("Fail. Threatening unsuccessful")

            amt = int(THREATEN_COST * self.apocalypse.mult["threaten_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy threatening")

        elif choice_str == GameMenu.STEAL:
            # Pick place
            locs = self.party.display_occupied_locations()
            choice = pick_option("From which location do you want to steal?", locs)
            vals = []
            for _ in range(NUM_DEFENDING_CHANCES):
                vals.append(randint(1, choice.protection.value))
            defending = max(vals)
            attacking = randint(0, self.party.steal_skill.value)
            if defending < attacking:
                print("Success!")
                cons = int(choice.consumables / 2)
                sups = int(choice.supplies / 2)
                choice.consumables -= cons
                choice.supplies -= sups
                self.party.consumables += cons
                self.party.supplies += sups
                print(f"Got half their consumables ({cons}) and supplies ({sups})")
            else:
                print("Fail. Stealing unsuccessful")

            amt = int(STEAL_COST * self.apocalypse.mult["steal_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy stealing")

        elif choice_str == GameMenu.INCREASE_COMFORT:
            amt = int(COMFORT_ADD_AMOUNT * self.party.settled.comfort.percent)
            self.party.settled.comfort.add_amount(amt)
            print(f"Added {amt} to comfort")
            print(f"Used {SUPPLIES_NEEDED_TO_BUILD} supplies")

            amt = int(BUILD_COST * self.apocalypse.mult["build_comfort_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy improving comfort")

        elif choice_str == GameMenu.INCREASE_PROTECTION:
            amt = int(PROTECTION_ADD_AMOUNT * self.party.settled.protection.percent)
            self.party.settled.protection.add_amount(amt)
            print(f"Added {amt} to protection")
            print(f"Used {SUPPLIES_NEEDED_TO_BUILD} supplies")

            amt = int(BUILD_COST * self.apocalypse.mult["build_protection_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy improving protection")

        elif choice_str == GameMenu.ABANDON:
            self.party.abandon_location()

            amt = int(ABANDON_COST * self.apocalypse.mult["abandon_cost"])
            self.party.energy.adjust_amount(-amt)
            print(f"Spent {amt} energy abandoning location")

        elif choice_str == GameMenu.QUIT:
            self.game_over()

        else:
            print("*" * 10, choice_str, "TYPO")

    def game_over(self):
        print(f"You have died. You lasted {self.day_number} days.")
        self.persist["name"] = "jordan"
        self.persist["score"] = self.day_number
        self.next_state = "HIGH_SCORES"
        self.playing = False

    def pass_day(self, number_of_days=1):
        for day in range(number_of_days):
            for house in self.party.scouted:
                house.protection.decay()
                house.comfort.decay()

            self.party.daily_energy_adjust(REST_ADD_AMOUNT)
            self.party.attitude.decay()

            self.day_number += 1

            input(colored(f"Time passes. It is now day {self.day_number}", "dim"))
            print()

        print()

    def deciding_loop(self):
        clear()
        self.print_header()
        options = self.present_options()
        choice = pick_option("How do you survive today?", options)
        self.implement(choice)

    def run(self):
        clear()

        while self.playing:
            self.days_to_pass = 1
            self.deciding_loop()
            if self.playing:
                self.pass_day(self.days_to_pass)
            if self.party.energy.value == 0:
                self.game_over()
        # exit()

    def cleanup(self):
        """Upon leaving state"""
        pass
