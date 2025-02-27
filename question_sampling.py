import itertools
import random
import pandas as pd

route_safety_levels = ["Well-maintained bike lanes", "Mixed safety", "No dedicated bike lanes"]
time_efficiency_levels = ["15 minutes", "20 minutes", "30 minutes"]
bicycle_facilities_levels = ["Secure parking and showers", "Basic parking, no showers", "No parking or showers"]

all_combinations = list(itertools.product(route_safety_levels, time_efficiency_levels, bicycle_facilities_levels))
random.shuffle(all_combinations)

def balanced_scenario_selection(combinations, num_scenarios):
    num_levels = num_scenarios // len(combinations[0])
    
    counters = {
        "Route Safety": {level: 0 for level in route_safety_levels},
        "Time Efficiency": {level: 0 for level in time_efficiency_levels},
        "Bicycle Facilities": {level: 0 for level in bicycle_facilities_levels}
    }
    
    selected_scenarios = []
    
    for comb in combinations:
        rs, te, bf = comb
        if (counters["Route Safety"][rs] < num_levels and
            counters["Time Efficiency"][te] < num_levels and
            counters["Bicycle Facilities"][bf] < num_levels):
            selected_scenarios.append({
                "Route Safety": rs,
                "Time Efficiency": te,
                "Bicycle Facilities": bf
            })
            counters["Route Safety"][rs] += 1
            counters["Time Efficiency"][te] += 1
            counters["Bicycle Facilities"][bf] += 1
        if len(selected_scenarios) == num_scenarios:
            break
    
    return selected_scenarios

num_scenarios = 12
selected_scenarios = balanced_scenario_selection(all_combinations, num_scenarios)
scenarios_df = pd.DataFrame(selected_scenarios)
scenarios_df.to_csv("resources/balanced_scenarios.csv", index=False)
