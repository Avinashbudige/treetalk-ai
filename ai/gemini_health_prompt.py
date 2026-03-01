"""
gemini_health_prompt.py
------------------------
Constructs system and analysis prompts for Gemini AI to diagnose tree health
from sensor data and provide actionable recommendations.
"""


def get_system_prompt():
    """
    Returns the system prompt that sets Gemini's role and behavior.
    """
    return """You are TreeTalk AI, an expert arborist and tree health specialist integrated with IoT sensor data analysis. 

Your purpose is to:
1. Interpret real-time sensor readings from trees
2. Diagnose health conditions with scientific precision
3. Communicate findings in clear, non-technical language anyone can understand
4. Provide immediate and long-term recommendations

You must:
- Always cite which sensor readings led to your diagnosis
- Use a severity level: CRITICAL (immediate action needed), WARNING (address within days), CAUTION (monitor), HEALTHY (no action needed)
- Provide 3-5 specific, actionable recommendations
- Acknowledge any limitations in remote diagnosis
- Encourage professional arborist consultation for critical issues
- Be empathetic - you're giving a voice to a living tree"""


def get_analysis_prompt(sensor_data: dict, tree_name: str = "Unknown Tree") -> str:
    """
    Generates a specific analysis prompt for the given sensor readings.
    
    Args:
        sensor_data: Dictionary containing all sensor readings
        tree_name: Name identifier for the tree
        
    Returns:
        Formatted analysis prompt string
    """
    
    # Format sensor data for readability
    sensor_str = "\n".join([f"  • {key.replace('_', ' ').title()}: {value} {_get_unit(key)}" 
                            for key, value in sensor_data.items()])
    
    prompt = f"""
Analyze the following real-time sensor readings from a tree and provide a comprehensive health report.

**Tree Identifier:** {tree_name}
**Reading Timestamp:** {sensor_data.get('timestamp', 'Current')}

**Sensor Readings:**
{sensor_str}

**Healthy Reference Ranges:**
  • Soil Moisture: 50-70%
  • Soil Temperature: 15-25°C
  • Soil pH: 6.0-7.5
  • Soil EC: 1.0-2.0 mS/cm
  • Air Temperature: 15-30°C
  • Air Humidity: 40-80%
  • Light (LUX): 10,000-50,000 lux
  • CO2: 380-420 ppm
  • Sap Flow: 1.5-3.0 L/hr
  • Trunk Diameter: Stable or slow growth
  • Leaf Temperature: 2-5°C above air temp
  • Vibration Amplitude: < 0.1g
  • Rainfall (24h): 0-10mm
  • Wind Speed: 5-25 km/h

**Your Task:**

1. **Health Status Overview** (1-2 sentences)
   - Give a brief, understandable summary of the tree's current state

2. **Identified Issues** (if any)
   - For each deviation from healthy ranges, explain what it indicates
   - Cross-reference multiple sensors for pattern confirmation
   - Classify severity: CRITICAL | WARNING | CAUTION | HEALTHY

3. **Root Cause Analysis**
   - What combinations of sensor readings suggest the problem?
   - Is this acute (sudden) or chronic (ongoing)?

4. **Immediate Recommendations** (Next 24-72 hours)
   - 2-3 specific actions the tree caretaker should take now

5. **Long-term Care Plan** (Next 2-4 weeks)
   - 2-3 actions to restore or maintain health

6. **Monitoring Alerts**
   - Which 2-3 sensors should be watched most closely?
   - What values would trigger urgent action?

7. **Professional Consultation?**
   - At current state, does this tree need an arborist visit? Why/why not?

**Format your response as a readable report, not technical jargon. Imagine you're texting a tree caretaker, not a botanist.**
"""
    
    return prompt.strip()


def _get_unit(sensor_key: str) -> str:
    """Helper to get the unit of measurement for each sensor."""
    units = {
        "soil_moisture_pct": "%",
        "soil_temperature_c": "°C",
        "soil_ph": "",
        "soil_ec_mS_cm": "mS/cm",
        "air_temperature_c": "°C",
        "air_humidity_pct": "%",
        "light_lux": "lux",
        "co2_ppm": "ppm",
        "trunk_diameter_mm": "mm",
        "sap_flow_L_hr": "L/hr",
        "leaf_temperature_c": "°C",
        "vibration_amplitude_g": "g",
        "rainfall_mm_24h": "mm",
        "wind_speed_km_h": "km/h",
    }
    return units.get(sensor_key, "")


def get_quick_reference_guide() -> str:
    """
    Returns a quick reference guide for interpreting common sensor patterns.
    Useful for validation before sending to Gemini.
    """
    return """
QUICK INTERPRETATION GUIDE:

🔴 DROUGHT STRESS PATTERN:
   - Low soil moisture (<30%)
   - High soil temperature (>30°C)
   - Low sap flow (<1 L/hr)
   - High leaf temperature (>30°C)
   → Action: Increase watering immediately

🔵 OVERWATERING PATTERN:
   - High soil moisture (>85%)
   - Cool soil (<15°C)
   - Low pH (<5.5)
   - Low sap flow (<0.5 L/hr)
   → Action: Reduce watering, improve drainage

🐛 PEST INFESTATION PATTERN:
   - High vibration (>0.3g)
   - Reduced sap flow
   - Slightly stressed sensors
   → Action: Visual inspection, consider treatment

📊 NUTRIENT DEFICIENCY PATTERN:
   - Low soil EC (<0.5 mS/cm)
   - Low pH acidic (<5.5)
   - Small trunk diameter growth
   - Slow sap flow
   → Action: Soil treatment, fertilization

✅ HEALTHY PATTERN:
   - All sensors in normal ranges
   - Smooth daily cycles
   - Stable vibration
   → Action: Continue current care, monitor weekly
"""
