from os import path
import pickle

from state import State
from utility import clear, pick_option, colored

MAX_HIGH_SCORES = 10


class HighScoresState(State):
    def __init__(self):
        super().__init__()
        self.next_state = None
        self.max_high_scores = MAX_HIGH_SCORES
        self.persist = {}
        self.scoreboard = []

    @property
    def highscore(self):
        return 0 if self.scoreboard == [] else self.scoreboard[0][1]

    def startup(self, persistent={}):
        """Upon state startup"""
        self.next_state = self
        self.persist = persistent
        self.scoreboard = self.load_scores()

        if self.persist.get("score", None):
            self.check_score(self.persist["score"], self.persist["name"])

    def load_scores(self):
        # load high score
        try:
            with open(path.join("data", "scoreboard.dat"), "rb") as file:
                scoreboard = pickle.load(file)
        except Exception:
            scoreboard = []
        return scoreboard

    def save_scores(self):
        with open(path.join("data", "scoreboard.dat"), "wb") as file:
            pickle.dump(self.scoreboard, file)

    def check_score(self, new_score, initials="JMK"):
        # Add Score
        self.scoreboard.append((initials, new_score))
        # Sort and limit to to 10
        self.scoreboard.sort(key=lambda tup: tup[1], reverse=True)
        if len(self.scoreboard) >= self.max_high_scores:
            self.scoreboard = self.scoreboard[: self.max_high_scores]
        # Save Scoreboard
        self.save_scores()

    def run(self):
        """Draw state"""
        print(colored("High Scores", "underline"))
        if self.scoreboard:
            for num, (name, score) in enumerate(self.scoreboard, 1):
                print(f"{num}. {name.ljust(18)} \t\t\t{score}")
        else:
            print("No high scores currently.")
        print()
        input("Press enter to return to main menu.")
        self.next_state = "MAIN_MENU"

    def cleanup(self):
        """Upon leaving state"""
        pass
