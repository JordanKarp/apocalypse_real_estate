from menu_options import ApocalypseMenu, PartyMenu
from apocalypse import Apocalypse
from party import Party
from state import State
from utility import clear, pick_option, colored


class GameSetupState(State):
    def __init__(self):
        super().__init__()

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent

    def print_header(self):
        print(colored("Game Setup", "underline"))

    def pick_apocalypse(self):
        options = ApocalypseMenu.list()
        print("Apocalypse: ")
        for num, apoc in enumerate(options, 1):
            print(f"{num}. {apoc}")
        choice = pick_option("Which apocalypse would you like to survive?", options)

        self.persist["apocalypse"] = Apocalypse.load_scenario(choice)

    def pick_party(self):
        options = PartyMenu.list()
        print("Party: ")
        for num, party in enumerate(options, 1):
            print(f"{num}. {party}")
        choice = pick_option("Choose your starting party: ", options)

        if choice == PartyMenu.EASY:
            party = Party().easy()
        elif choice == PartyMenu.AVERAGE:
            party = Party().average()
        elif choice == PartyMenu.HARD:
            party = Party().hard()
        elif choice == PartyMenu.RANDOM:
            party = Party().random()
        else:
            party = Party()
        self.persist["party"] = party

    def run(self):
        clear()
        self.print_header()
        self.pick_apocalypse()
        self.pick_party()
        input("Press enter to start. ")
        self.next_state = "GAME"

    def cleanup(self):
        """Upon leaving state"""
        pass
