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
        print("Game Instructions go here.....")
        print()

    def run(self):
        clear()
        self.print_help()
        input("Press enter to return to main menu. ")
        self.next_state = "MAIN_MENU"

    def cleanup(self):
        """Upon leaving state"""
        pass
