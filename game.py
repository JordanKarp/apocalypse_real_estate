from random import randint

from daily_log import DailyLog
from location import Location
from menu_options import GameMenu
from map import Map
from party import Party
from utility import clear, colored, pick_option, create_table, proceed
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
        self.map = None
        self.party = None
        self.log = None
        self.locations = []

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent
        self.apocalypse = self.persist.get("apocalypse", "Pandemic")
        self.party = self.persist.get("party", Party())
        self.map = self.persist.get("map", Map().new_map())
        self.log = self.persist.get("log", DailyLog())

    def print_header(self):
        print("-" * 5, f"Day {self.day_number} - {self.apocalypse.name}", "-" * 5)
        self.party.display_full_stats()
        print("-" * 28)

    def present_options(self):
        options = [
            (GameMenu.SHOW_LOG, 0, 0),
            (GameMenu.SHOW_MAP, 0, 0),
            (GameMenu.SHOW_INVENTORY, 0, 0),
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
                options.extend(
                    (
                        (
                            GameMenu.SETTLE,
                            int(SETTLE_COST * self.apocalypse.mult["settle_cost"]),
                            SUPPLIES_NEEDED_TO_BUILD,
                        ),
                        (
                            GameMenu.SCAVENGE,
                            int(SCAVENGE_COST * self.apocalypse.mult["scavenge_cost"]),
                            0,
                        ),
                    )
                )
        if self.party.settled:
            options.append(
                (
                    GameMenu.BUILD_PROTECTION,
                    int(BUILD_COST * self.apocalypse.mult["build_protection_cost"]),
                    SUPPLIES_NEEDED_TO_BUILD,
                )
            )
            options.extend(
                (
                    (
                        GameMenu.BUILD_COMFORT,
                        int(BUILD_COST * self.apocalypse.mult["build_comfort_cost"]),
                        SUPPLIES_NEEDED_TO_BUILD,
                    ),
                    (
                        GameMenu.ABANDON,
                        int(ABANDON_COST * self.apocalypse.mult["abandon_cost"]),
                        0,
                    ),
                )
            )
        options.append((GameMenu.QUIT, None, None))

        table = [["#", "Description", "Energy", "Supplies"]]
        for num, (opt, cost, sup) in enumerate(options, 1):
            if isinstance(cost, (int, str)):
                table.append([f"{num}.", opt, cost, sup])
            else:
                table.append([f"{num}.", opt, "", ""])

        print(create_table(table, True))
        return [opt for opt, _, _ in options]

    def implement(self, choice_str):
        if choice_str == GameMenu.NOTHING:
            return
        # DISPLAY OPTIONS
        if choice_str == GameMenu.SHOW_SCOUTED:
            self.party.display_scouted_locations()
            proceed()
            self.deciding_loop()

        elif choice_str == GameMenu.SHOW_LOG:
            self.log.print_log()
            proceed()
            self.deciding_loop()

        elif choice_str == GameMenu.SHOW_INVENTORY:

            self.party.inventory.add_item(
                "Can of Sardines", 1, 1, "Good to eat, not so enjoyable."
            )
            print(self.party.inventory)
            proceed()
            self.deciding_loop()

        elif choice_str == GameMenu.SHOW_PARTY:
            self.party.display_full_stats()
            proceed()
            self.deciding_loop()

        elif choice_str == GameMenu.SHOW_MAP:
            self.map.draw_map()
            proceed()
            self.deciding_loop()

        elif choice_str == GameMenu.IMPROVE:
            self.party.display_party_skills(enumerate=True)
            choice = pick_option(
                "Which skill would you like to improve?", self.party.skills
            )
            choice.adjust_amount(SKILL_ADD_AMOUNT)
            self.log.add_entry(
                self.day_number, f"{choice.name} was improved by {SKILL_ADD_AMOUNT}"
            )
            # print(f"{choice.name} was improved by {SKILL_ADD_AMOUNT}")
            # print(choice)

            amt = int(IMPROVE_COST * self.apocalypse.mult["improve_cost"])
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(
                self.day_number, "Spent {amt} energy improving {choice.name}"
            )
            # print(f"Spent {amt} energy improving {choice.name}")

        elif choice_str == GameMenu.TRAVEL:
            self.days_to_pass = TRAVEL_DAYS * self.apocalypse.mult["travel_cost"]
            self.party.travel(self.days_to_pass)
            self.log.add_entry(
                self.day_number,
                f"{self.days_to_pass} days will pass on your journey to a new area.",
            )
            # TODO FIX
            self.map = Map.new_map()

        elif choice_str == GameMenu.SCOUT:
            # TODO make better than adding 1-3 random locations
            new_locs = int(MAX_SCOUT * self.party.scout_skill.percent)
            locs = []
            for _ in range(new_locs):
                location = Location.random_location()
                self.party.scouted.append(location)
                locs.append(location)
            self.log.add_entry(self.day_number, f"{new_locs} new location(s) found.")
            # print(f"{new_locs} new location(s) found.")
            for loc in locs:
                print("\t-", loc)

            amt = int(SCOUT_COST * self.apocalypse.mult["scout_cost"])
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(self.day_number, f"Spent {amt} energy scouting")
            # print(f"Spent {amt} energy scouting")

        elif choice_str == GameMenu.SETTLE:
            locs = self.party.display_unoccupied_locations()
            choice = pick_option("Which location to settle?", locs)
            self.party.settle_location(choice)
            self.log.add_entry(self.day_number, f"{choice.address} has been settled.")
            # print(choice.address, "has been settled.")

            amt = int(SETTLE_COST * self.apocalypse.mult["settle_cost"])
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(
                self.day_number, f"Spent {amt} energy settling new location."
            )

            # print(f"Spent {amt} energy settling new location.")

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
            amt = supply if choice.supplies >= supply else choice.supplies
            self.party.supplies += amt
            self.log.add_entry(self.day_number, f"Gained {amt} supplies.")

            amt = consume if choice.consumables >= consume else choice.supplies
            self.party.consumables += amt
            self.log.add_entry(self.day_number, f"Gained {amt} consumables.")

            # Remove rest of materials
            choice.consumables = 0
            choice.supplies = 0
            # Fix lists
            self.party.scouted.remove(choice)
            self.party.scavenged.append(choice)

            amt = SCAVENGE_COST * self.apocalypse.mult["scavenge_cost"]
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(self.day_number, f"Spent {amt} energy scavenging")

        elif choice_str == GameMenu.BUILD_COMFORT:
            amt = int(COMFORT_ADD_AMOUNT * self.party.settled.comfort.percent)
            self.party.settled.comfort.add_amount(amt)
            self.log.add_entry(self.day_number, f"Added {amt} to comfort")
            self.log.add_entry(
                self.day_number, f"Used {SUPPLIES_NEEDED_TO_BUILD} supplies"
            )

            amt = int(BUILD_COST * self.apocalypse.mult["build_comfort_cost"])
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(self.day_number, "Spent {amt} energy improving comfort")

        elif choice_str == GameMenu.BUILD_PROTECTION:
            amt = int(PROTECTION_ADD_AMOUNT * self.party.settled.protection.percent)
            self.party.settled.protection.adjust_amount(amt)
            self.log.add_entry(self.day_number, f"Added {amt} to protection")
            self.log.add_entry(
                self.day_number, f"Used {SUPPLIES_NEEDED_TO_BUILD} supplies"
            )

            amt = int(BUILD_COST * self.apocalypse.mult["build_protection_cost"])
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(
                self.day_number, f"Spent {amt} energy improving protection"
            )

        elif choice_str == GameMenu.ABANDON:
            self.log.add_entry(self.day_number, f"Left {self.party.settled.address}.")
            self.party.abandon_location()

            amt = int(ABANDON_COST * self.apocalypse.mult["abandon_cost"])
            self.party.energy.adjust_amount(-amt)
            self.log.add_entry(
                self.day_number, f"Spent {amt} energy abandoning location"
            )

        elif choice_str == GameMenu.QUIT:
            self.game_over()

        else:
            print("*" * 10, choice_str, "TYPO")

    def game_over(self):
        self.log.add_entry(
            self.day_number, f"You have died. You lasted {self.day_number} days."
        )
        self.persist["name"] = "jordan"
        self.persist["score"] = self.day_number
        self.next_state = "HIGH_SCORES"
        self.playing = False

    def pass_day(self, number_of_days=1):
        for _ in range(number_of_days):
            # FIX TO all houses
            for house in self.party.scouted:
                house.protection.decay()
                house.comfort.decay()

            msg = self.party.daily_energy_adjust(REST_ADD_AMOUNT)
            self.log.add_entry(self.day_number, msg)
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
