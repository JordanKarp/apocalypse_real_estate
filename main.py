from game import Game
from game_setup import GameSetupState
from help import HelpState
from high_scores import HighScoresState
from main_menu import MainMenuState
from options import OptionsState
from state_manager import StateManager


def run():
    states = {
        "MAIN_MENU": MainMenuState(),
        "OPTIONS": OptionsState(),
        "HELP": HelpState(),
        "HIGH_SCORES": HighScoresState(),
        "GAME_SETUP": GameSetupState(),
        "GAME": Game(),
    }

    game_manager = StateManager(states, "MAIN_MENU")
    game_manager.run()


if __name__ == "__main__":
    run()
