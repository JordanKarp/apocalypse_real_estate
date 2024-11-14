class StateManager:
    def __init__(self, states, starting_state):
        self.states = states
        self.state_name = starting_state
        self.current_state = self.states[self.state_name]
        self.flip_state(self.state_name)
        self.previous_state_name = None

    def flip_state(self, specified_state=None):
        """Handles changing states properly.

        Args:
            specified_state(str): Defines the state to flip to. If None, flips to previous state.
        """
        if not specified_state:
            specified_state = self.previous_state_name
        self.current_state.cleanup()
        persistent = self.current_state.persist
        self.previous_state_name = self.state_name
        self.state_name = specified_state
        self.current_state = self.states[self.state_name]
        self.current_state.startup(persistent)

    def run(self):
        """Main Program Loop"""
        while True:
            if self.current_state != self.current_state.next_state:
                if self.current_state.next_state == "QUIT":
                    break
                self.flip_state(self.current_state.next_state)

            self.current_state.run()
