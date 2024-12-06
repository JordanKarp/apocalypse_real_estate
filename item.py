class Item:
    def __init__(self, name, quantity, weight, description):
        self.name = name
        self.quantity = quantity
        self.weight = weight
        self.description = description

    def __str__(self):
        return (
            f"{self.name} (x{self.quantity}, {self.weight}kg each): {self.description}"
        )
