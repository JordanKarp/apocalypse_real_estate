from dataclasses import dataclass, field


@dataclass
class Apocalypse:
    name: str = "Zombies"
    mult: dict = field(
        default_factory=lambda: {
            "scout_cost": 1,
            "improve_cost": 1,
            "settle_cost": 1,
            "scavenge_cost": 1,
            "travel_cost": 1,
            "negotiate_cost": 1,
            "threaten_cost": 1,
            "steal_cost": 1,
            "build_protection_cost": 1,
            "build_comfort_cost": 1,
            "abandon_cost": 1,
        }
    )

    @classmethod
    def load_scenario(cls, scenario_name):
        scenarios = {
            "Pandemic": {
                "scout_cost": 2,
                "improve_cost": 2,
                "settle_cost": 2,
                "scavenge_cost": 2,
                "travel_cost": 2,
                "negotiate_cost": 2,
                "threaten_cost": 2,
                "steal_cost": 2,
                "build_protection_cost": 2,
                "build_comfort_cost": 2,
                "abandon_cost": 2,
            },
            "Hurricane": {
                "scout_cost": 1.5,
                "improve_cost": 1.5,
                "settle_cost": 1.5,
                "scavenge_cost": 1.5,
                "travel_cost": 1.5,
                "negotiate_cost": 1.5,
                "threaten_cost": 1.5,
                "steal_cost": 1.5,
                "build_protection_cost": 1.5,
                "build_comfort_cost": 1.5,
                "abandon_cost": 1.5,
            },
            "Impact Winter": {
                "scout_cost": 3,
                "improve_cost": 3,
                "settle_cost": 3,
                "scavenge_cost": 3,
                "travel_cost": 3,
                "negotiate_cost": 3,
                "threaten_cost": 3,
                "steal_cost": 3,
                "build_protection_cost": 3,
                "build_comfort_cost": 3,
                "abandon_cost": 3,
            },
        }

        if scenario_name in scenarios:
            return cls(scenario_name, scenarios[scenario_name])
        else:
            raise ValueError(
                "Scenario not found. Available scenarios: "
                + ", ".join(scenarios.keys())
            )


# class Apocalypse:
#     def __init__(self, name, multipliers):
#         """
#         Initializes the Apocalypse scenario with a name and a dictionary of multipliers.

#         Parameters:
#         - name (str): The name of the apocalypse scenario.
#         - multipliers (dict): A dictionary with multipliers for each parameter.
#         """
#         self.name = name
#         self.multipliers = multipliers

#     @classmethod
#     def load_scenario(cls, scenario_name):
#         scenarios = {
#             "nuclear_winter": {
#                 "health": 0.8,
#                 "morale": 0.6,
#                 "food_supply": 0.5,
#                 "water_supply": 0.4,
#                 "energy": 0.7,
#                 "shelter_quality": 0.9,
#                 "protection_level": 1.2,
#                 "infection_risk": 1.5,
#             },
#             "pandemic": {
#                 "health": 0.5,
#                 "morale": 0.7,
#                 "food_supply": 0.8,
#                 "water_supply": 1.0,
#                 "energy": 0.9,
#                 "infection_risk": 2.0,
#                 "shelter_quality": 1.1,
#                 "communication_ability": 0.7,
#             },
#             "alien_invasion": {
#                 "health": 0.9,
#                 "morale": 0.8,
#                 "protection_level": 1.5,
#                 "energy": 0.8,
#                 "stealth_visibility": 1.3,
#                 "communication_ability": 1.2,
#                 "mental_resilience": 0.8,
#             },
#             "climate_catastrophe": {
#                 "health": 0.7,
#                 "morale": 0.6,
#                 "food_supply": 0.6,
#                 "water_supply": 0.7,
#                 "shelter_quality": 1.2,
#                 "protection_level": 1.1,
#                 "equipment_durability": 0.8,
#             },
#             "grey_goo": {
#                 "health": 0.6,
#                 "morale": 0.5,
#                 "food_supply": 0.5,
#                 "water_supply": 0.5,
#                 "supplies": 0.3,
#                 "protection_level": 1.5,
#                 "equipment_durability": 0.5,
#             },
#         }
#         if scenario_name in scenarios:
#             return cls(scenario_name, scenarios[scenario_name])
#         else:
#             raise ValueError(
#                 "Scenario not found. Available scenarios: "
#                 + ", ".join(scenarios.keys())
#             )
