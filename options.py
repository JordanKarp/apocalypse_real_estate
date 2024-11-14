from menu_options import OptionsMenu
from state import State
from utility import clear, pick_option, colored


class OptionsState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent

    def print_header(self):
        print(colored("Options Menu", "underline"))
        for num, opt in enumerate(OptionsMenu.list(), 1):
            print(f"{num}. {opt}")

    def run(self):
        clear()
        self.print_header()
        choice = pick_option("", OptionsMenu.list())
        if choice == OptionsMenu.DEFAULT_NAME:
            name = input("What is your name? ")
            self.persist["NAME"] = name
            print(f"{name} confirmed as new default name")
            input("Press enter to proceed.")
        elif choice == OptionsMenu.BACK:
            self.next_state = "MAIN_MENU"

    def cleanup(self):
        """Upon leaving state"""
        pass
