"""
test_api.py
-----------
Basic tests for the TreeTalk AI FastAPI server.
Run with: pytest tests/ -v
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "TreeTalk AI"
    assert "endpoints" in data

def test_list_scenarios():
    response = client.get("/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
    assert "healthy" in data["scenarios"]
    assert "drought_stress" in data["scenarios"]

def test_list_trees():
    response = client.get("/trees")
    assert response.status_code == 200
    data = response.json()
    assert "trees" in data
    assert data["count"] >= 1

def test_mock_analyze_healthy():
    response = client.get("/mock-analyze/healthy")
    assert response.status_code == 200
    data = response.json()
    assert "sensors" in data
    assert "scenario" in data
    assert data["scenario"] == "healthy"

def test_mock_analyze_drought():
    response = client.get("/mock-analyze/drought_stress")
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "drought_stress"
    assert "report" in data

def test_mock_analyze_invalid_scenario():
    response = client.get("/mock-analyze/unknown_scenario")
    assert response.status_code == 400

def test_post_analyze():
    payload = {
        "tree_id": "TEST-001",
        "species": "Ficus benghalensis",
        "age_years": 10,
        "sensors": {
            "soil_moisture_pct": 18.5,
            "soil_temperature_c": 35.0,
            "air_temperature_c": 38.0,
            "air_humidity_pct": 28.0,
            "light_lux": 65000,
            "co2_ppm": 405,
            "sap_flow_L_hr": 0.4,
            "vibration_amplitude_g": 0.02,
        },
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tree_id"] == "TEST-001"
    assert "report" in data

def test_mock_analyze_all_scenarios():
    scenarios = ["healthy", "drought_stress", "overwatering", "pest_infestation", "nutrient_deficiency"]
    for scenario in scenarios:
        response = client.get(f"/mock-analyze/{scenario}")
        assert response.status_code == 200, f"Failed for scenario: {scenario}"