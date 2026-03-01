"""
mock_sensor_readings.py
-----------------------
Simulates IoT sensor data from a tree health monitoring system.
Covers 5 scenarios: healthy, drought_stress, overwatering,
pest_infestation, nutrient_deficiency.
"""

import random
import json
from datetime import datetime


SCENARIOS = {
    "healthy": {
        "soil_moisture_pct":        (55, 70),
        "soil_temperature_c":       (18, 22),
        "soil_ph":                  (6.0, 7.0),
        "soil_ec_mS_cm":            (1.0, 2.0),
        "air_temperature_c":        (20, 28),
        "air_humidity_pct":         (50, 65),
        "light_lux":                (30000, 60000),
        "co2_ppm":                  (400, 450),
        "trunk_diameter_mm":        (150, 155),
        "sap_flow_L_hr":            (1.5, 3.0),
        "leaf_temperature_c":       (22, 27),
        "vibration_amplitude_g":    (0.01, 0.05),
        "rainfall_mm_24h":          (0, 5),
        "wind_speed_km_h":          (5, 20),
    },
    "drought_stress": {
        "soil_moisture_pct":        (10, 25),
        "soil_temperature_c":       (28, 38),
        "soil_ph":                  (6.5, 7.5),
        "soil_ec_mS_cm":            (2.0, 3.5),
        "air_temperature_c":        (32, 42),
        "air_humidity_pct":         (20, 35),
        "light_lux":                (50000, 80000),
        "co2_ppm":                  (380, 420),
        "trunk_diameter_mm":        (140, 148),
        "sap_flow_L_hr":            (0.2, 0.8),
        "leaf_temperature_c":       (35, 42),
        "vibration_amplitude_g":    (0.01, 0.04),
        "rainfall_mm_24h":          (0, 0),
        "wind_speed_km_h":          (15, 40),
    },
    "overwatering": {
        "soil_moisture_pct":        (85, 100),
        "soil_temperature_c":       (14, 18),
        "soil_ph":                  (5.0, 6.0),
        "soil_ec_mS_cm":            (0.2, 0.8),
        "air_temperature_c":        (18, 24),
        "air_humidity_pct":         (75, 95),
        "light_lux":                (5000, 20000),
        "co2_ppm":                  (450, 500),
        "trunk_diameter_mm":        (152, 160),
        "sap_flow_L_hr":            (0.1, 0.5),
        "leaf_temperature_c":       (18, 23),
        "vibration_amplitude_g":    (0.01, 0.03),
        "rainfall_mm_24h":          (30, 80),
        "wind_speed_km_h":          (2, 10),
    },
    "pest_infestation": {
        "soil_moisture_pct":        (45, 60),
        "soil_temperature_c":       (20, 26),
        "soil_ph":                  (6.0, 7.0),
        "soil_ec_mS_cm":            (1.0, 2.0),
        "air_temperature_c":        (22, 30),
        "air_humidity_pct":         (50, 70),
        "light_lux":                (25000, 55000),
        "co2_ppm":                  (410, 460),
        "trunk_diameter_mm":        (148, 153),
        "sap_flow_L_hr":            (0.5, 1.5),
        "leaf_temperature_c":       (24, 30),
        "vibration_amplitude_g":    (0.15, 0.45),
        "rainfall_mm_24h":          (0, 10),
        "wind_speed_km_h":          (5, 25),
    },
    "nutrient_deficiency": {
        "soil_moisture_pct":        (40, 60),
        "soil_temperature_c":       (18, 24),
        "soil_ph":                  (4.5, 5.5),
        "soil_ec_mS_cm":            (0.1, 0.5),
        "air_temperature_c":        (20, 28),
        "air_humidity_pct":         (45, 65),
        "light_lux":                (20000, 45000),
        "co2_ppm":                  (390, 440),
        "trunk_diameter_mm":        (143, 150),
        "sap_flow_L_hr":            (0.8, 1.8),
        "leaf_temperature_c":       (22, 28),
        "vibration_amplitude_g":    (0.01, 0.05),
        "rainfall_mm_24h":          (0, 8),
        "wind_speed_km_h":          (5, 20),
    },
}

OPTIMAL_RANGES = {
    "soil_moisture_pct":     "50-70 %",
    "soil_temperature_c":    "15-25 C",
    "soil_ph":               "6.0-7.0",
    "soil_ec_mS_cm":         "1.0-2.0 mS/cm",
    "air_temperature_c":     "15-30 C",
    "air_humidity_pct":      "40-70 %",
    "light_lux":             "20000-60000 lux",
    "co2_ppm":               "400-450 ppm",
    "trunk_diameter_mm":     "stable / slight diurnal swing",
    "sap_flow_L_hr":         "1.0-3.0 L/hr",
    "leaf_temperature_c":    "20-30 C",
    "vibration_amplitude_g": "< 0.08 g (higher = pest activity)",
    "rainfall_mm_24h":       "0-15 mm/day",
    "wind_speed_km_h":       "0-40 km/h",
}

def generate_reading(scenario: str = "healthy", tree_id: str = "TREE-001") -> dict:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario '{scenario}'. Choose from: {list(SCENARIOS)}")

    ranges = SCENARIOS[scenario]
    reading = {
        "tree_id":   tree_id,
        "scenario":  scenario,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "location": {
            "lat":  12.9716,
            "lon":  77.5946,
            "site": "Cubbon Park - Plot A3",
        },
        "species":   "Ficus benghalensis",
        "age_years": 25,
        "sensors":   {},
        "optimal_ranges": OPTIMAL_RANGES,
    }

    for key, (lo, hi) in ranges.items():
        value = round(random.uniform(lo, hi) + random.gauss(0, (hi - lo) * 0.02), 3)
        reading["sensors"][key] = value

    return reading

def run_demo():
    print("=" * 65)
    print("  TreeTalk AI - Mock Sensor Demo")
    print(f"  Generated at: {datetime.utcnow().isoformat()}Z")
    print("=" * 65)

    for scenario in SCENARIOS:
        reading = generate_reading(scenario)
        print(f"\n  Scenario : {scenario.upper().replace('_', ' ')}")
        print(f"    Tree ID  : {reading['tree_id']}")
        print(f"    Species  : {reading['species']}")
        print(f"    Location : {reading['location']['site']}")
        print("    Sensors  :")
        for k, v in reading["sensors"].items():
            optimal = OPTIMAL_RANGES.get(k, "")
            print(f"      {k:<30} {v:>10}   (optimal: {optimal})")

    print("\n" + "=" * 65)
    print("  Full JSON for 'drought_stress':")
    print("=" * 65)
    print(json.dumps(generate_reading("drought_stress"), indent=2))

if __name__ == "__main__":
    run_demo()
