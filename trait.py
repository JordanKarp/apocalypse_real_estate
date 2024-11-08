from dataclasses import dataclass


@dataclass
class Trait:
    name: str = "TraitName"
    _value: int = 100
    max_value: int = 100
    decay_rate: float = 1.0

    @property
    def value(self):
        if self._value > self.max_value:
            self._value = self.max_value
        if self._value < 0:
            self._value = 0
        return self._value

    def decay(self, modifier=1):
        self._value -= self.decay_rate * modifier

    def adjust_amount(self, amount, modifier=1):
        self._value += amount * modifier

    def __str__(self):
        val = f"\033[32m{self.value}/{self.max_value}\033[00m"
        return f"{self.name}: ({val})"

    def __repr__(self):
        return f"{self.value}/{self.max_value}"
