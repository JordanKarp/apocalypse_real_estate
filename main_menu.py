import pickle
from pathlib import Path

from menu_options import MainMenu
from state import State
from utility import clear, pick_option, colored

SAVES_PATH = Path(".") / "saves"


class MainMenuState(State):
    def __init__(self):
        super().__init__()
        self.persist["saves_path"] = SAVES_PATH

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent

    def print_header(self):
        print(colored("Welcome to Real Estate: Apocalypse", "underline"))
        for num, opt in enumerate(MainMenu.list(), 1):
            print(f"{num}. {opt}")
        # print(MainMenu.list())

    # def load_user(self, name):
    #     while True:
    #         try:
    #             filename = f"{name}.dat"
    #             with open(SAVES_PATH / filename, "rb") as f:
    #                 user_data = pickle.load(f)
    #         except FileNotFoundError:
    #             print("Game not found, starting a new game instead?")
    #             play = input("[y/n]\n")
    #             if play in ["y", "Y"]:
    #                 return User(name)
    #             else:
    #                 name = self.prompt_name()
    #         else:
    #             return user_data

    def run(self):
        clear()
        self.print_header()
        choice = pick_option("", MainMenu.list())
        try:
            if choice == MainMenu.NEW:
                self.next_state = "GAME_SETUP"
            elif choice == MainMenu.LOAD:
                raise NotImplementedError
            elif choice == MainMenu.OPTIONS:
                self.next_state = "OPTIONS"
            elif choice == MainMenu.HELP:
                self.next_state = "HELP"
            elif choice == MainMenu.HIGH_SCORES:
                self.next_state = "HIGH_SCORES"
            elif choice == MainMenu.QUIT:
                exit()
        except Exception:
            print("Not Implemented")
            input("")

    def cleanup(self):
        """Upon leaving state"""
        pass
