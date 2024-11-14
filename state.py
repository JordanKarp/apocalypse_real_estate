class State:
    """Default class for a game state"""

    def __init__(self):
        """Init"""
        self.next_state = None
        self.persist = {}

    def startup(self, persistent=None):
        """Upon state startup"""
        if persistent is None:
            persistent = {}
        self.next_state = self
        self.persist = persistent

    def run(self):
        """Running the state"""
        pass

    def cleanup(self):
        """Upon leaving state"""
        pass
