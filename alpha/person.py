from dataclasses import dataclass, field

FOOD_LOSS = 10
COMFORT_LOSS = 5
MAX = 100

WORK_WEEK_HOURS = 168
DOWNTIME = 0.8


@dataclass
class Trait:
    name: str = "TraitName"
    _value: int = 100
    max_value: int = 100

    @property
    def value(self):
        if self._value > self.max_value:
            self._value = self.max_value
        return self._value

    def __str__(self):
        return f"{self.name}: ({self.value}/{self.max_value})"

    def __repr__(self):
        return f"{self.value}/{self.max_value}"


@dataclass
class Person:
    name: str = "Guy"
    food: Trait = Trait("Food", 80, 100)
    comfort: Trait = Trait("Comfort", 80, 100)
    schedule: list = field(default_factory=lambda: [])

    multipliers: dict = field(
        default_factory=lambda: {
            "eat": 1.0,
            "sleep": 2.0,
            "relax": 1.0,
            "work": 1.0,
        }
    )

    def do_task(self, task, amount):
        if task == "eat":
            self.food._value += amount * self.multipliers[task]
        elif task == "sleep":
            self.comfort._value += amount * self.multipliers[task]
        elif task == "relax":
            self.comfort._value += amount * self.multipliers[task]
        elif task == "work":
            self.food._value -= amount * self.multipliers[task]
            self.comfort._value -= amount * self.multipliers[task]

    def elapse_week(self):
        for task, amount in self.schedule:
            self.do_task(task, amount)


p = Person()
# p.do_task("eat", 10)
# p.do_task("sleep", 10)
p.do_task("work", 10)
print(p)
