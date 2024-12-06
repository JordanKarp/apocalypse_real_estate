from item import Item


class Inventory:
    def __init__(self, max_weight):
        self.items = {}  # Use a dictionary for items
        self.max_weight = max_weight
        self.weight_unit = "Lbs"

    def current_weight(self):
        """Calculate the current total weight of the inventory."""
        return sum(item.quantity * item.weight for item in self.items.values())

    def can_add_item(self, weight_to_add):
        """Check if adding weight_to_add would exceed max weight."""
        return self.current_weight() + weight_to_add <= self.max_weight

    def add_item(self, name, quantity, weight, description):
        """Add an item to the inventory, respecting the weight limit."""
        weight_to_add = quantity * weight
        if not self.can_add_item(weight_to_add):
            return f"Cannot add {name} (x{quantity}): Exceeds weight limit!"

        if name in self.items:
            self.items[name].quantity += quantity
            return f"Updated quantity of {name} to {self.items[name].quantity}."
        else:
            self.items[name] = Item(name, quantity, weight, description)
            return f"Added {quantity}x {name} to inventory."

    def remove_item(self, name, quantity):
        """Remove an item from the inventory."""
        if name in self.items:
            item = self.items[name]
            if item.quantity < quantity:
                return f"Not enough {name} to remove. Only {item.quantity} available."
            item.quantity -= quantity
            if item.quantity == 0:
                del self.items[name]  # Remove item if quantity is zero
            return f"Removed {quantity}x {name} from inventory."
        return f"Item {name} not found in inventory."

    def list_inventory(self):
        """List all items in the inventory."""
        if not self.items:
            return "Inventory is empty."
        return "\n".join(f" - {str(item)}" for item in self.items.values())

    def summary(self):
        return f"Inventory: ({self.current_weight()} / {self.max_weight}{self.weight_unit})"

    def __str__(self):
        """String representation of the inventory."""
        return self.summary() + "\n" + self.list_inventory()


# inv = Inventory(100)

# print(inv.add_item("Can of Sardines", 1, 1, "Good to eat, not so enjoyable."))
# print(inv.add_item("Can of Sardines", 1, 1, "Good to eat, not so enjoyable."))
# print(inv.add_item("Can Opener", 1, 2, "Who knew this was so important?"))
# print(inv)
