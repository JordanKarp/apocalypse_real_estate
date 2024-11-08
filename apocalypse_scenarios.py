from enum import Enum


class ApocalypseScenarios(str, Enum):
    PANDEMIC = "Pandemic"
    HURRICANE = "Hurricane"
    WINTER = "Impact Winter"

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
