# 🌳 TreeTalk AI - MVP Quick Start Guide

This guide will help you get the MVP (Minimum Viable Product) running in 5 minutes.

---

## 🎯 What's the MVP?

The MVP consists of:
1. **Sensor Data Generator** (`sensors/mock_sensor_readings.py`) - Simulates 5 tree health scenarios
2. **Gemini AI Prompts** (`ai/gemini_health_prompt.py`) - Expert arborist system + analysis prompts
3. **REST API** (`api/main.py`) - FastAPI backend with 2 analysis endpoints

**Core Flow:**
```
Sensor Data → Gemini AI (with TreeTalk prompt) → Human-Readable Health Report
```

---

## 🚀 Installation & Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/Avinashbudige/treetalk-ai.git
cd treetalk-ai
pip install -r requirements.txt
```

### 2. Get Your Gemini API Key
- Go to: https://aistudio.google.com/app/apikey
- Click **"Create API Key"** (free tier available)
- Copy the key

### 3. Set Up Environment
```bash
cp .env.example .env
```

Then edit `.env` and paste your Gemini API key:
```env
GEMINI_API_KEY=paste_your_key_here
```

---

## 🧪 Test the MVP

### Option A: Test with Mock Data (No real sensors needed)

```bash
# Terminal 1: Start the API server
python -m uvicorn api.main:app --reload

# Terminal 2: Test an endpoint
curl http://localhost:8000/mock-analyze/healthy?tree_name="Oak%20Tree"
```

This will:
1. Generate mock sensor data for a **healthy** tree
2. Send it to Gemini AI with the TreeTalk prompt
3. Return a detailed health report

### Option B: Test with Real Sensor Data

Once you have real sensor data from your IoT setup:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "soil_moisture_pct": 55,
    "soil_temperature_c": 20,
    "soil_ph": 6.5,
    "soil_ec_mS_cm": 1.5,
    "air_temperature_c": 25,
    "air_humidity_pct": 60,
    "light_lux": 40000,
    "co2_ppm": 420,
    "trunk_diameter_mm": 152,
    "sap_flow_L_hr": 2.0,
    "leaf_temperature_c": 26,
    "vibration_amplitude_g": 0.05,
    "rainfall_mm_24h": 2,
    "wind_speed_km_h": 12,
    "tree_name": "My Oak Tree"
  }'
```

---

## 📡 Available API Endpoints (MVP)

### 1. **Health Check**
```bash
GET http://localhost:8000/
```
Returns project info and all available endpoints.

### 2. **Mock Analysis** (TEST MODE)
```bash
GET http://localhost:8000/mock-analyze/{scenario}?tree_name=MyTree
```

**Scenarios available:**
- `healthy` - Normal conditions
- `drought_stress` - Dry soil, high temperature
- `overwatering` - Wet soil, low light
- `pest_infestation` - High vibration (trunk shaking)
- `nutrient_deficiency` - Low soil nutrients

**Example:**
```bash
curl http://localhost:8000/mock-analyze/drought_stress?tree_name="Pine%20Tree"
```

**Response:**
```json
{
  "tree_name": "Pine Tree",
  "timestamp": "2026-03-01T15:30:45.123456",
  "health_status": "Mock Analysis: drought_stress",
  "analysis": "[Full health report from Gemini AI...]",
  "severity": "WARNING"
}
```

### 3. **Real Analysis** (PRODUCTION MODE)
```bash
POST http://localhost:8000/analyze
Content-Type: application/json

{
  "soil_moisture_pct": 55,
  "soil_temperature_c": 20,
  ...all 14 sensor values...
  "tree_name": "Oak Tree",
  "timestamp": "2026-03-01T15:30:00Z"
}
```

### 4. **List Scenarios**
```bash
GET http://localhost:8000/scenarios
```

---

## 🤖 The TreeTalk Prompt

The MVP uses a sophisticated prompt system with two components:

### 1. **System Prompt** (Role Definition)
Sets Gemini as an expert arborist and defines behavior:
- Interpret sensor readings
- Diagnose health conditions
- Provide actionable recommendations
- Use citizen-friendly language

### 2. **Analysis Prompt** (Per-Tree Specifics)
Includes:
- All sensor readings for the tree
- Healthy reference ranges
- Task breakdown (health status, issues, recommendations, alerts)
- Format requirements (readable report, not technical)

**Example output format:**
```
Health Status Overview: The tree appears moderately stressed...

Identified Issues:
  • CRITICAL: Soil moisture is 15% (healthy range: 50-70%)
  • WARNING: Soil temperature elevated at 35°C...

Root Cause Analysis:
  The low soil moisture + high temperature suggest...

Immediate Recommendations (Next 24-72 hours):
  1. Water the tree deeply...
  2. Apply...
  3. Monitor...

Long-term Care Plan...
```

---

## 📊 How It Works (Detailed)

```
┌─────────────────────┐
│  Sensor Data        │
│  (14 values)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  analysis_prompt generates:             │
│  • Tree name & timestamp                │
│  • All sensor values                    │
│  • Healthy reference ranges             │
│  • Analysis task breakdown              │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  Gemini 1.5 Pro with:                   │
│  • system_prompt (expert arborist role) │
│  • analysis_prompt (specific tree data) │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Health Report      │
│  • Status overview  │
│  • Issue breakdown  │
│  • Recommendations  │
│  • Severity level   │
└─────────────────────┘
```

---

## 🔍 Interpreting Results

The Gemini response includes severity levels:

| Severity | Meaning | Action |
|----------|---------|--------|
| **HEALTHY** | All sensors normal | Continue monitoring weekly |
| **CAUTION** | Minor deviations | Monitor closely, adjust care |
| **WARNING** | Significant issues | Take action within days |
| **CRITICAL** | Tree at risk | **Immediate action needed** |

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY not set"
✅ Solution: Edit `.env` and add your key (from step 3 above)

### "Connection refused" on /analyze
✅ Solution: Make sure the API server is running (`python -m uvicorn api.main:app --reload`)

### "Invalid scenario"
✅ Solution: Use one of: healthy, drought_stress, overwatering, pest_infestation, nutrient_deficiency

### "Gemini API error"
✅ Solutions:
   - Verify API key is correct
   - Check you have free tier quota remaining
   - Try a different scenario

---

## 📈 Next Steps After MVP

1. **Connect Real Sensors** - Replace mock data with actual IoT readings
2. **Build Dashboard** - Create React frontend to visualize data
3. **Alert System** - SMS/Email notifications for CRITICAL issues
4. **Multi-Tree Network** - Monitor 100s of trees simultaneously
5. **Historical Logging** - Store data in a database for trends

---

## 📞 Need Help?

- Check the main [README.md](README.md)
- Open an issue: https://github.com/Avinashbudige/treetalk-ai/issues
- See example data: `examples/real_reading.json`

---

## ✅ MVP Checklist

- [x] Mock sensor data generator (5 scenarios)
- [x] Gemini prompt system (system + analysis)
- [x] REST API (2 endpoints: `/analyze`, `/mock-analyze`)
- [x] Severity classification (CRITICAL/WARNING/CAUTION/HEALTHY)
- [x] Human-readable health reports
- [ ] Real IoT integration (coming soon)
- [ ] Dashboard UI (coming soon)
- [ ] Alert notifications (coming soon)

---

**"Give trees a voice before it's too late."** 🌳
