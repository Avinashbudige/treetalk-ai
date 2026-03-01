"""
main.py
-------
FastAPI backend for TreeTalk AI.

MVP Endpoints:
  - POST /analyze → Send sensor data, get tree health report from Gemini
  - GET /mock-analyze/{scenario} → Test with mock data
"""

import os
import json
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from pydantic import BaseModel

from sensors.mock_sensor_readings import generate_sensor_data, SCENARIOS
from ai.gemini_health_prompt import get_system_prompt, get_analysis_prompt


# Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please add it to .env")

genai.configure(api_key=API_KEY)

# Initialize FastAPI app
app = FastAPI(
    title="TreeTalk AI",
    description="IoT sensors + Gemini AI for real-time tree health monitoring",
    version="0.1.0",
)


# ============================================================================
# DATA MODELS
# ============================================================================

class SensorData(BaseModel):
    """Schema for sensor data input."""
    soil_moisture_pct: float
    soil_temperature_c: float
    soil_ph: float
    soil_ec_mS_cm: float
    air_temperature_c: float
    air_humidity_pct: float
    light_lux: float
    co2_ppm: float
    trunk_diameter_mm: float
    sap_flow_L_hr: float
    leaf_temperature_c: float
    vibration_amplitude_g: float
    rainfall_mm_24h: float
    wind_speed_km_h: float
    tree_name: Optional[str] = "Unknown Tree"
    timestamp: Optional[str] = None


class HealthReport(BaseModel):
    """Schema for health analysis response."""
    tree_name: str
    timestamp: str
    health_status: str
    analysis: str
    severity: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check and project info."""
    return {
        "status": "🌳 TreeTalk AI is listening...",
        "version": "0.1.0 (MVP)",
        "endpoints": {
            "analyze": "POST /analyze (send real sensor data)",
            "mock_analyze": "GET /mock-analyze/{scenario}",
            "scenarios": "GET /scenarios",
        }
    }


@app.post("/analyze")
async def analyze_sensor_data(sensor_data: SensorData) -> HealthReport:
    """
    MVP Endpoint: Analyze real sensor data.
    
    Sends sensor readings to Google Gemini AI for health diagnosis.
    
    Args:
        sensor_data: Complete sensor readings from the tree
        
    Returns:
        HealthReport with diagnosis and recommendations
    """
    
    try:
        # Prepare sensor data as dictionary
        sensor_dict = sensor_data.dict()
        timestamp = sensor_dict.get("timestamp") or datetime.now().isoformat()
        tree_name = sensor_dict.get("tree_name", "Unknown Tree")
        
        # Generate analysis prompt
        analysis_prompt = get_analysis_prompt(sensor_dict, tree_name)
        
        # Call Gemini AI with system and analysis prompts
        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=get_system_prompt()
        )
        
        response = model.generate_content(analysis_prompt)
        analysis_text = response.text
        
        # Extract severity from response for quick reference
        severity = "UNKNOWN"
        if "CRITICAL" in analysis_text:
            severity = "CRITICAL"
        elif "WARNING" in analysis_text:
            severity = "WARNING"
        elif "CAUTION" in analysis_text:
            severity = "CAUTION"
        elif "HEALTHY" in analysis_text:
            severity = "HEALTHY"
        
        return HealthReport(
            tree_name=tree_name,
            timestamp=timestamp,
            health_status="Analyzed",
            analysis=analysis_text,
            severity=severity
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/mock-analyze/{scenario}")
async def mock_analyze(scenario: str, tree_name: Optional[str] = "Test Tree") -> HealthReport:
    """
    MVP Endpoint: Test analysis with mock data.
    
    Generates mock sensor data for a specific scenario and analyzes it.
    
    Args:
        scenario: One of [healthy, drought_stress, overwatering, 
                         pest_infestation, nutrient_deficiency]
        tree_name: Name for the tree
        
    Returns:
        HealthReport with diagnosis and recommendations
    """
    
    if scenario not in SCENARIOS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unknown scenario. Available: {list(SCENARIOS.keys())}"
        )
    
    try:
        # Generate mock sensor data
        sensor_dict = generate_sensor_data(scenario)
        sensor_dict["tree_name"] = tree_name
        sensor_dict["timestamp"] = datetime.now().isoformat()
        
        # Generate analysis prompt
        analysis_prompt = get_analysis_prompt(sensor_dict, tree_name)
        
        # Call Gemini AI
        model = genai.GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=get_system_prompt()
        )
        
        response = model.generate_content(analysis_prompt)
        analysis_text = response.text
        
        # Extract severity
        severity = "UNKNOWN"
        if "CRITICAL" in analysis_text:
            severity = "CRITICAL"
        elif "WARNING" in analysis_text:
            severity = "WARNING"
        elif "CAUTION" in analysis_text:
            severity = "CAUTION"
        elif "HEALTHY" in analysis_text:
            severity = "HEALTHY"
        
        return HealthReport(
            tree_name=tree_name,
            timestamp=sensor_dict["timestamp"],
            health_status=f"Mock Analysis: {scenario}",
            analysis=analysis_text,
            severity=severity
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mock analysis failed: {str(e)}")


@app.get("/scenarios")
async def get_scenarios():
    """List all available mock scenarios for testing."""
    return {
        "scenarios": list(SCENARIOS.keys()),
        "description": "Use these with GET /mock-analyze/{scenario}"
    }


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Verify Gemini API connection on startup."""
    try:
        test_model = genai.GenerativeModel("gemini-1.5-pro")
        response = test_model.generate_content("Respond with 'OK' if you're working.")
        if response.text:
            print("✅ Gemini AI connection verified")
    except Exception as e:
        print(f"⚠️  Warning: Could not verify Gemini API: {e}")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
