from random import randint

from apocalypse import Apocalypse
from apocalypse_scenarios import ApocalypseScenarios
from location import Location
from menu_options import Menu
from party import Party
from utility import clear, colored


REST_ADD_AMOUNT = 5
SKILL_ADD_AMOUNT = 5
DEFAULT_SCAV = 10
PROTECTION_ADD_AMOUNT = 5
COMFORT_ADD_AMOUNT = 5
NEGOTIATE_CHANCE = 0.75


class Game:
    def __init__(self):
        self.playing = True
        self.day_number = 1
        self.days_to_pass = 1
        self.apocalypse = Apocalypse.load_scenario("pandemic")
        self.party = Party()
        self.locations = []

        # # DEBUG Prefilled scouted locations
        # for _ in range(NUM_LOCATIONS):
        #     self.party.scouted.append(Location.random_location())

    def print_header(self):
        print("-" * 10, f"Day {self.day_number}", "-" * 10)
        self.party.display_party_stats()
        print("-" * 28)

    def present_options(self):
        options = [
            Menu.SHOW_SCOUTED,
            Menu.SHOW_PARTY,
            Menu.NOTHING,
            Menu.SCOUT,
            Menu.IMPROVE,
        ]
        if self.party.scouted:
            if any(not loc.occupied for loc in self.party.scouted):
                # if len(self.party.scouted) >= 1:
                options.append(Menu.SETTLE)
                options.append(Menu.SCAVENGE)
                if not self.party.settled:
                    options.append(Menu.TRAVEL)
            if any(loc.occupied for loc in self.party.scouted):
                options.append(Menu.NEGOTIATE)
                options.append(Menu.THREATEN)
                options.append(Menu.STEAL)

        if self.party.settled:
            options.append(Menu.IMPROVE_COMFORT)
            options.append(Menu.IMPROVE_PROTECTION)
            options.append(Menu.ABANDON)

        options.append(Menu.QUIT)

        for num, opt in enumerate(options, 1):
            print(f"{num}. {opt}")

        return options

    def pick_option(self, prompt, given_list):
        print(prompt)
        choice = input("--> ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(given_list):
                choice -= 1
                return given_list[choice]
            else:
                print("Invalid choice. Please try again.")
                return self.pick_option(prompt, given_list)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.pick_option(prompt, given_list)

    def implement(self, choice_str):
        # DISPLAY OPTIONS
        if choice_str == Menu.SHOW_SCOUTED:
            self.party.display_scouted_locations()
            input("Press enter to return to menu.")
            self.deciding_loop()

        elif choice_str == Menu.SHOW_PARTY:
            self.party.display_full_stats()
            input("Press enter to return to menu.")
            self.deciding_loop()

        elif choice_str == Menu.NOTHING:
            pass

        elif choice_str == Menu.IMPROVE:
            self.party.display_party_skills(enumerate=True)
            choice = self.pick_option(
                "Which skill would you like to improve?", self.party.skills
            )
            choice.adjust_amount(SKILL_ADD_AMOUNT)
            print(f"{choice} was improved by {SKILL_ADD_AMOUNT}")

        elif choice_str == Menu.TRAVEL:
            self.days_to_pass = 3
            print("3 days pass on your journey.")

        elif choice_str == Menu.SCOUT:
            # TODO make better than adding 1-3 random locations
            new_locs = randint(1, 3)
            for _ in range(new_locs):
                self.party.scouted.append(Location.random_location())
            print(f"{new_locs} new location(s) found.")

            # ! Add improve cost cost
            self.party.energy.adjust_amount(-10)

        elif choice_str == Menu.SETTLE:
            locs = self.party.display_unoccupied_locations()
            choice = self.pick_option("Which location to settle?", locs)
            self.party.settle_location(choice)
            self.party.scouted.remove(choice)
            print(choice.address, "has been settled.")
            # ! Add Settle cost

        elif choice_str == Menu.SCAVENGE:
            # Pick place
            locs = self.party.display_unoccupied_locations()
            choice = self.pick_option("Which location to scavage?", locs)
            # Determine amount to scavenge
            amount_to_scav = int(DEFAULT_SCAV * (self.party.scavenge_skill / 100))
            # Split between food and supplys
            consume = randint(1, amount_to_scav)
            supply = amount_to_scav - consume
            # gain amount, or as much as they have of each type
            if choice.supplies >= supply:
                amt = supply
            else:
                amt = choice.supplies
            self.party.supplies += amt

            if choice.consumables >= consume:
                amt = consume
            else:
                amt = choice.supplies
            self.party.consumables += amt

            # Remove rest of materials
            choice.consumables = 0
            choice.supplies = 0
            # Fix lists
            self.party.scouted.remove(choice)
            self.party.scavenged.append(choice)
            # ! Add Scavenge cost

        elif choice_str == Menu.NEGOTIATE:
            # Pick place
            locs = self.party.display_occupied_locations()
            choice = self.pick_option(
                "With which location do you want to negotiate?", locs
            )
            success_chance = NEGOTIATE_CHANCE * (self.party.charisma_skill.value / 100)
            print(success_chance)

        elif choice_str == Menu.THREATEN:
            pass

        elif choice_str == Menu.STEAL:
            pass

        elif choice_str == Menu.IMPROVE_COMFORT:
            # TODO fix to be affected by apocalypse
            self.party.settled.comfort.add_amount(COMFORT_ADD_AMOUNT)
            # ! Add comfort cost

        elif choice_str == Menu.IMPROVE_PROTECTION:
            # TODO fix to be affected by apocalypse
            self.party.settled.protection.add_amount(PROTECTION_ADD_AMOUNT)
            # ! Add protection cost

        elif choice_str == Menu.ABANDON:
            self.party.settled = None
            # ! Add Abandon cost

        elif choice_str == Menu.QUIT:
            print(f"You have died. You lasted {self.day_number} days.")
            self.playing = False

        else:
            print("*" * 10, choice_str, "TYPO")

    def pass_day(self, number_of_days=1):
        for house in self.party.scouted:
            house.protection.decay()
            house.comfort.decay()

        self.party.daily_energy_adjust(REST_ADD_AMOUNT)
        self.party.attitude.decay()

        print("Time passes")
        input(colored("Time passes.....", "dim"))
        print()

        print()

    def deciding_loop(self):
        clear()
        self.print_header()
        options = self.present_options()
        choice = self.pick_option("How do you survive today?", options)
        self.implement(choice)

    def intro_text(self):
        print("Welcome to Real Estate Apocalypse!")

    def pick_apocalypse_scenario(self):
        options = ApocalypseScenarios.list()
        for num, apoc in enumerate(ApocalypseScenarios, 1):
            print(f"{num}. {apoc.value}")
        choice = self.pick_option(
            "Which apocalypse would you like to survive?", options
        )
        print(choice)

    def print_apocalypse_intro_text(self):
        print("details of the scenario here:")

    def run(self):
        clear()
        self.intro_text()
        self.pick_apocalypse_scenario()
        self.print_apocalypse_intro_text()
        while self.playing:
            self.days_to_pass = 1
            self.deciding_loop()
            if self.playing:
                self.pass_day(self.days_to_pass)
                self.day_number += self.days_to_pass


game = Game()

game.run()
