# 🌳 TreeTalk AI - MVP Summary

## What Was Generated

This document summarizes the **Minimum Viable Product (MVP)** that has been created for TreeTalk AI.

---

## 📦 Core Components Created

### 1. **Gemini AI Prompt System** (`ai/gemini_health_prompt.py`)

The heart of the MVP - a sophisticated prompt system that guides Google Gemini to act as an expert arborist.

**Components:**

#### a) System Prompt
Sets Gemini's role and behavior:
- Expert arborist + IoT analyst
- Multi-language communication (non-technical)
- Severity levels (CRITICAL, WARNING, CAUTION, HEALTHY)
- Evidence-based diagnosis with sensor citations
- Actionable recommendations

**Key characteristics:**
```python
- Role: Expert arborist + tree health specialist
- Input: Real-time sensor readings
- Output: Clear, non-technical health reports
- Empathy: "Give trees a voice"
```

#### b) Analysis Prompt
Dynamically generated for each tree with:
- Specific sensor values
- Healthy reference ranges (10 sensors)
- Structured task breakdown:
  1. Health Status Overview
  2. Identified Issues (severity classification)
  3. Root Cause Analysis
  4. Immediate Recommendations (24-72 hours)
  5. Long-term Care Plan (2-4 weeks)
  6. Monitoring Alerts
  7. Professional Consultation Guidance

#### c) Helper Functions
- `_get_unit()` - Converts sensor keys to units (°C, %, lux, etc.)
- `get_quick_reference_guide()` - Pattern recognition for validation

### 2. **REST API Backend** (`api/main.py`)

FastAPI-based backend with two main analysis endpoints.

**Key Features:**

#### Endpoints:
| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Health check & endpoint info |
| `GET` | `/scenarios` | List available test scenarios |
| `GET` | `/mock-analyze/{scenario}` | Test with mock sensor data |
| `POST` | `/analyze` | Real sensor analysis |

#### Data Validation:
- Pydantic `SensorData` model for input validation
- 14 sensor types validated
- Optional tree_name and timestamp

#### Error Handling:
- HTTPException for invalid scenarios
- Gemini API error handling
- Proper HTTP status codes

#### Response Format:
```python
{
  "tree_name": str,
  "timestamp": str,
  "health_status": str,
  "analysis": str (full report),
  "severity": str (CRITICAL|WARNING|CAUTION|HEALTHY)
}
```

### 3. **Enhanced Sensor Module** (`sensors/mock_sensor_readings.py`)

Added the `generate_sensor_data()` function to export flat sensor dictionaries for the API.

**New Function:**
```python
def generate_sensor_data(scenario, tree_id) -> dict
```
Returns 14 sensor values in a flat dictionary format needed by the API.

---

## 🔄 Data Flow (MVP)

```
┌─────────────────────────────────────────────────────────────┐
│                    TreeTalk AI MVP Flow                      │
└─────────────────────────────────────────────────────────────┘

User Request
    ↓
POST /analyze (or GET /mock-analyze/{scenario})
    ↓
┌──────────────────────────────────────────────────┐
│  Sensor Data Generation                          │
│  - Mock: Generate 14 sensor values               │
│  - Real: Accept from IoT sensors                 │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  Prompt Generation                               │
│  - System Prompt: Define Gemini as arborist      │
│  - Analysis Prompt: Include sensor data +        │
│    healthy ranges + task breakdown               │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  Gemini 1.5 Pro Processing                       │
│  - Analyze sensor patterns                       │
│  - Compare to healthy ranges                     │
│  - Synthesize health assessment                  │
│  - Generate natural language report              │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│  Response Formatting                             │
│  - Extract severity level                        │
│  - Package in HealthReport schema                │
│  - Return JSON                                   │
└──────────────────────────────────────────────────┘
    ↓
HTTP 200 JSON Response
```

---

## 📊 Sensors & Ranges

The MVP monitors **14 sensors** with these healthy ranges:

| Sensor | Unit | Healthy Range | Indicates |
|--------|------|---------------|-----------|
| soil_moisture_pct | % | 50-70 | Root hydration |
| soil_temperature_c | °C | 15-25 | Soil warmth |
| soil_ph | - | 6.0-7.5 | Soil acidity |
| soil_ec_mS_cm | mS/cm | 1.0-2.0 | Soil conductivity |
| air_temperature_c | °C | 15-30 | Ambient temp |
| air_humidity_pct | % | 40-80 | Moisture in air |
| light_lux | lux | 10k-50k | Sunlight intensity |
| co2_ppm | ppm | 380-420 | Atmospheric CO₂ |
| trunk_diameter_mm | mm | ~150 | Growth indicator |
| sap_flow_L_hr | L/hr | 1.5-3.0 | Tree vitality |
| leaf_temperature_c | °C | App temp + 2-5°C | Leaf stress |
| vibration_amplitude_g | g | <0.1 | Pest/wind damage |
| rainfall_mm_24h | mm | 0-10 | Recent water |
| wind_speed_km_h | km/h | 5-25 | Environmental stress |

---

## 🧪 Test Scenarios

The MVP includes 5 pre-defined scenarios for testing without real sensors:

### 1. **HEALTHY** ✅
- All sensors in normal ranges
- What a thriving tree looks like

### 2. **DROUGHT_STRESS** 🏜️
- Low soil moisture (10-25%)
- High temperature (28-38°C)
- Low sap flow (0.2-0.8 L/hr)
- Pattern: Tree needs water urgently

### 3. **OVERWATERING** 💧
- High soil moisture (85-100%)
- Cool soil (14-18°C)
- Low pH (5.0-6.0)
- Pattern: Root damage risk, poor drainage

### 4. **PEST_INFESTATION** 🐛
- High vibration amplitude (0.15-0.45g)
- Reduced sap flow (0.5-1.5 L/hr)
- Otherwise normal ranges
- Pattern: Bark/leaf damage

### 5. **NUTRIENT_DEFICIENCY** ⚠️
- Very low soil EC (0.1-0.5 mS/cm)
- Acidic pH (4.5-5.5)
- Small trunk growth (143-150mm)
- Pattern: Stunted growth, weak sap flow

---

## 🎯 MVP Capabilities

### What It Can Do:
- ✅ Analyze real sensor data in real-time
- ✅ Generate human-readable health reports
- ✅ Classify severity levels (CRITICAL → HEALTHY)
- ✅ Test with 5 mock scenarios
- ✅ Provide immediate & long-term recommendations
- ✅ Identify root causes from sensor patterns
- ✅ Suggest professional arborist consultation
- ✅ Process multiple trees sequentially

### What It Cannot Do (Future):
- ❌ Real IoT sensor integration (needs hardware)
- ❌ Web dashboard (coming soon)
- ❌ SMS/Email alerts (future)
- ❌ Multi-tree real-time monitoring (coming)
- ❌ Historical trend analysis (needs database)
- ❌ Predictive alerts (needs ML)

---

## 🚀 How to Use

### Quick Start:
```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your Gemini API key

# 3. Run API
python -m uvicorn api.main:app --reload

# 4. Test (in another terminal)
python test_mvp.py
```

### Test an Endpoint:
```bash
# Mock analysis
curl http://localhost:8000/mock-analyze/healthy?tree_name="Oak%20Tree"

# Real analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"soil_moisture_pct": 55, ...}' 
```

---

## 📁 MVP File Structure

```
treetalk-ai/
├── ai/
│   ├── __init__.py
│   └── gemini_health_prompt.py      ← 🆕 Prompt system (162 lines)
├── api/
│   ├── __init__.py                  ← 🆕 New folder
│   └── main.py                      ← 🆕 FastAPI backend (254 lines)
├── sensors/
│   ├── mock_sensor_readings.py       ← Updated with generate_sensor_data()
│   └── __init__.py
├── tests/
│   └── test_api.py
├── examples/
│   └── real_reading.json
├── QUICKSTART.md                    ← 🆕 Quick start guide
├── test_mvp.py                      ← 🆕 Automated test suite
├── README.md
├── requirements.txt
└── .env.example
```

---

## 🔧 Technical Stack

- **AI Engine**: Google Gemini 1.5 Pro
- **Backend**: FastAPI 0.110.0
- **Validation**: Pydantic 2.6.4
- **HTTP Client**: httpx 0.27.0
- **Testing**: pytest 8.1.1

---

## 💡 Key Design Decisions

### 1. **Two-Part Prompt System**
- **System Prompt**: Defines Gemini's role (reusable, static)
- **Analysis Prompt**: Includes tree-specific data (dynamic, per-request)
- **Benefit**: Clear separation of concerns, easy to modify behavior

### 2. **Severity Classification**
- Extracted automatically from Gemini response
- Allows quick filtering of critical issues
- Enables future alert triggers

### 3. **Mock Data Support**
- Enables testing without real sensors
- 5 realistic scenarios for validation
- Helps debug prompt without API costs

### 4. **Flat Sensor Dictionary**
- API accepts simple key-value pairs
- Easy to connect to IoT devices
- Matches expected Pydantic model

### 5. **Reference Ranges Built-in**
- Included in every analysis prompt
- Consistent baseline across analyses
- Easy to update for different tree species

---

## 📈 Roadmap After MVP

**Phase 2: Real Sensors**
- Raspberry Pi integration
- Arduino sensor hub
- Real-time data streaming

**Phase 3: Dashboard**
- React.js frontend
- Live charts & graphs
- Location mapping

**Phase 4: Alerts**
- SMS notifications
- Email summaries
- Slack/Teams webhooks

**Phase 5: Network**
- Multi-tree dashboard
- Comparative analysis
- Community insights

---

## 🧠 Example: How Gemini Analyzes

**Input (Sensor Data):**
```
soil_moisture: 15%  (healthy: 50-70%)
sap_flow: 0.3 L/hr  (healthy: 1.5-3.0)
leaf_temp: 38°C     (healthy: ~25°C)
air_humidity: 25%   (healthy: 40-80%)
```

**Gemini Reasoning (from system prompt):**
1. "Sensor pattern shows drought symptoms"
2. "Low moisture + reduced sap = water stress"
3. "High leaf temp indicates stress response"

**Output (Report excerpt):**
```
Health Status: Tree is under severe drought stress.

CRITICAL: Soil moisture is critically low at 15% 
(healthy range: 50-70%). Combined with reduced sap flow 
(0.3 L/hr) and elevated leaf temperature (38°C), the tree 
is in immediate water stress.

Immediate Recommendations:
1. Water deeply within the next 24 hours (2-3x normal)
2. Mulch around base to retain moisture
3. Reduce direct sun exposure if possible

Severity: CRITICAL
```

---

## ✅ Validation & Testing

### Automated Test Suite (`test_mvp.py`)
Runs 4 tests:
1. ✅ Health check (`GET /`)
2. ✅ Get scenarios (`GET /scenarios`)
3. ✅ Mock analysis (`GET /mock-analyze/healthy`)
4. ✅ Real analysis (`POST /analyze`)

### Manual Testing
```bash
python test_mvp.py  # Runs all tests with color output
```

---

## 📝 Environment Variables

Required:
- **GEMINI_API_KEY** - Google Gemini API key (free tier available)

Optional:
- **SERVER_HOST** - API host (default: 0.0.0.0)
- **SERVER_PORT** - API port (default: 8000)
- **LOG_LEVEL** - Logging level (default: info)

---

## 🎓 Learning Resources

- **Gemini API**: https://aistudio.google.com
- **FastAPI**: https://fastapi.tiangolo.com
- **Pydantic**: https://docs.pydantic.dev

---

## 🌍 Open Source

This MVP is built as an open-source project to make tree health monitoring accessible to everyone.

- **License**: MIT
- **Repository**: https://github.com/Avinashbudige/treetalk-ai
- **Author**: Avinash Budige

---

## 🎯 Success Metrics for MVP

✅ **Achieved:**
- [x] Analyzes sensor data in real-time
- [x] Returns actionable health reports
- [x] Classifies severity levels correctly
- [x] Supports multiple test scenarios
- [x] Human-readable output
- [x] Minimal dependencies

📊 **Ready for:**
- [ ] Real IoT sensor integration
- [ ] Production deployment
- [ ] User testing

---

**"Give trees a voice before it's too late."** 🌳

For questions or contributions, visit: https://github.com/Avinashbudige/treetalk-ai
