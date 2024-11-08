from location import Location
from apocalypse import Apocalypse
from person import Person

NUM_PERSONS = 2
NUM_LOCATIONS = 5
DAYS_ELAPSED = 100


class Game:
    def __init__(self):
        self.playing = True
        self.inside = False
        self.apocalypse = Apocalypse()
        self.party = []
        self.locations = []

        for _ in range(NUM_LOCATIONS):
            self.locations.append(Location.random())
        for _ in range(NUM_PERSONS):
            self.party.append(Person())

    def print_locations(self):
        for num, loc in enumerate(self.locations, 1):
            print(f"{num}. {loc}")

    def run(self):
        while self.playing:
            if self.inside:
                pass
            else:
                # user turn
                self.print_locations()

                finished = input("Done with your turn? ")
                if finished.lower() in ["y", "yes"]:
                    self.playing = False

                # time elapsed
                print("Days pass....")


game = Game()

game.run()
