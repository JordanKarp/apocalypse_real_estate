from dataclasses import dataclass, field


@dataclass
class Apocalypse:
    name: str = "Zombies"
    effects: dict = field(
        default_factory=lambda: {
            "protection": -1,
            "comfort": -1,
            "food": -1,
        }
    )
