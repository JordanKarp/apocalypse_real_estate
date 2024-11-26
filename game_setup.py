from menu_options import ApocalypseMenu, PartyMenu
from apocalypse import Apocalypse
from map import Map
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

    def create_map(self):
        dimensions = (15, 90)
        num_buildings = 50
        game_map = Map(dimensions)
        # game_map.create_connected_roads(dimensions, 10, game_map.add_road)
        game_map.add_road(False, 4, 1, 84)
        game_map.add_road(False, 8, 25, 40)
        game_map.add_road(True, 3, 2, 8)
        game_map.add_road(False, 9, 5, 30)
        game_map.add_road(True, 1, 28, 20)
        game_map.add_buildings(num_buildings)

        self.persist["map"] = game_map

    def run(self):
        clear()
        self.print_header()
        self.pick_apocalypse()
        self.pick_party()
        self.create_map()
        input("Press enter to start. ")
        self.next_state = "GAME"

    def cleanup(self):
        """Upon leaving state"""
        pass
