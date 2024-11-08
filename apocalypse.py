class Apocalypse:
    def __init__(self, name, multipliers):
        """
        Initializes the Apocalypse scenario with a name and a dictionary of multipliers.

        Parameters:
        - name (str): The name of the apocalypse scenario.
        - multipliers (dict): A dictionary with multipliers for each parameter.
        """
        self.name = name
        self.multipliers = multipliers

    def apply_multipliers(self, stats):
        """
        Applies the apocalypse scenario multipliers to the provided stats.

        Parameters:
        - stats (dict): A dictionary of the party's current stats.

        Returns:
        - dict: A dictionary with the updated stats after applying multipliers.
        """
        updated_stats = {}
        for stat, value in stats.items():
            multiplier = self.multipliers.get(
                stat, 1
            )  # Default multiplier is 1 if not specified
            updated_stats[stat] = value * multiplier
        return updated_stats

    @classmethod
    def load_scenario(cls, scenario_name):
        scenarios = {
            "nuclear_winter": {
                "health": 0.8,
                "morale": 0.6,
                "food_supply": 0.5,
                "water_supply": 0.4,
                "energy": 0.7,
                "shelter_quality": 0.9,
                "protection_level": 1.2,
                "infection_risk": 1.5,
            },
            "pandemic": {
                "health": 0.5,
                "morale": 0.7,
                "food_supply": 0.8,
                "water_supply": 1.0,
                "energy": 0.9,
                "infection_risk": 2.0,
                "shelter_quality": 1.1,
                "communication_ability": 0.7,
            },
            "alien_invasion": {
                "health": 0.9,
                "morale": 0.8,
                "protection_level": 1.5,
                "energy": 0.8,
                "stealth_visibility": 1.3,
                "communication_ability": 1.2,
                "mental_resilience": 0.8,
            },
            "climate_catastrophe": {
                "health": 0.7,
                "morale": 0.6,
                "food_supply": 0.6,
                "water_supply": 0.7,
                "shelter_quality": 1.2,
                "protection_level": 1.1,
                "equipment_durability": 0.8,
            },
            "grey_goo": {
                "health": 0.6,
                "morale": 0.5,
                "food_supply": 0.5,
                "water_supply": 0.5,
                "supplies": 0.3,
                "protection_level": 1.5,
                "equipment_durability": 0.5,
            },
        }
        if scenario_name in scenarios:
            return cls(scenario_name, scenarios[scenario_name])
        else:
            raise ValueError(
                "Scenario not found. Available scenarios: "
                + ", ".join(scenarios.keys())
            )
