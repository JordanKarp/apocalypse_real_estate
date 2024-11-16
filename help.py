from menu_options import OptionsMenu
from state import State
from utility import clear, colored


class HelpState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent

    def print_help(self):
        print(colored("Help", "underline"))
        print()
        print("Survive during the apocalypse for as long as you can!")
        print()
        print(
            "Each day, you'll need to decide what action to take. Most actions cost energy, and some cost supplies, and some will take multiple days!"
        )
        print(
            "Once the day is over, you'll eat (if you have consumables) and rest (if you're settled in a location) to gain back energy."
        )
        print(
            "This is also when the apocalypse will affect you and the world around you."
        )
        print()
        print("Party Details:")
        print(
            " - Energy level: Ability to do things. The game is over if you run out of energy."
        )
        print("\t Energy is depleted daily based on this formula: TBD")
        print(" - Attitude level: Efficiency of the things you do.")
        print(" - Consumables: Food you have to eat.")
        print(" - Supplies: Materials to improve your location.")
        print(" - Scouted: List of nearby locations you have investigated.")

        print()
        print("Rundown of daily actions:")
        print("- Do nothing: Don't spend any energy today.")
        print("- Scout nearby home: See what homes are nearby.")
        print("- Improve Party: Increase one of your party skills.")
        print(
            "- Travel to a new area: Move to a new neighborhood, losing up all scouted locations."
        )
        print(
            "- Settle an unoccupied home: Move into home. Gain all the location's resources and supplies."
        )
        print(
            "- Scavenge an unoccupied home: Gather consumables and supplies from a nearby home."
        )
        print(
            "- Negotiate with another party: Convince another group to give you consumables and supplies"
        )
        print(
            "- Threaten another party: Intimidate another group to give you consumables and supplies"
        )
        print("- Steal from another party: Sneak in and take consumables and supplies")
        print(
            "- Build home comfort: Use supplies to increase your current home's comfort."
        )
        print(
            "- Build home protection: Use supplies to increase your current home's protection."
        )

    def run(self):
        clear()
        self.print_help()
        input("Press enter to return to main menu. ")
        self.next_state = "MAIN_MENU"

    def cleanup(self):
        """Upon leaving state"""
        pass
