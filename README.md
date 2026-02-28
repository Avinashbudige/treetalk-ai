# 🌳 TreeTalk AI

> **"Give trees a voice before it's too late."**

TreeTalk AI is an open-source project that uses IoT sensors embedded in trees combined with Google Gemini AI to monitor, diagnose, and communicate a tree's health status in real time — in plain language anyone can understand.

---

## 🌍 Why TreeTalk AI?

Trees are silent. By the time visible symptoms appear — yellowing leaves, bark damage, wilting — it is often too late to save them. TreeTalk AI gives trees an early-warning voice by:

- Continuously reading environmental and physiological sensor data
- Sending that data to Google Gemini AI for expert-level diagnosis
- Returning human-readable health reports with actionable recommendations
- Alerting caretakers before irreversible damage occurs

---

## 🏗️ Architecture

```
[IoT Sensors on Tree]
        │
        ▼
[Mock / Real Sensor Script]   ←──  sensors/mock_sensor_readings.py
        │
        ▼
[FastAPI Backend Server]      ←──  api/main.py
        │
        ▼
[Gemini 1.5 Pro AI Engine]    ←──  ai/gemini_health_prompt.py
        │
        ▼
[Health Report + Alerts]      ←──  JSON response / dashboard / SMS
```

---

## 📡 Sensors Used

| Sensor | Measures | Healthy Range |
|--------|----------|---------------|
| Soil Moisture | Root hydration (%) | 40 – 70 % |
| Temperature | Ambient temperature (°C) | 15 – 30 °C |
| Humidity | Air humidity (%) | 40 – 80 % |
| Light (LUX) | Sunlight intensity | 10,000 – 50,000 lux |
| pH Sensor | Soil acidity | 6.0 – 7.5 |
| Nitrogen (N) | Soil nitrogen level (mg/kg) | 20 – 40 mg/kg |
| Phosphorus (P) | Soil phosphorus (mg/kg) | 15 – 25 mg/kg |
| Potassium (K) | Soil potassium (mg/kg) | 100 – 200 mg/kg |
| Vibration | Trunk micro-vibrations (Hz) | less than 5 Hz |
| CO2 | Leaf-level CO2 (ppm) | 400 – 800 ppm |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key (https://aistudio.google.com/app/apikey)

### Installation

```bash
git clone https://github.com/Avinashbudige/treetalk-ai.git
cd treetalk-ai
pip install -r requirements.txt
cp .env.example .env
python sensors/mock_sensor_readings.py
uvicorn api.main:app --reload
```

---

## 📁 Project Structure

```
treetalk-ai/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── sensors/
│   └── mock_sensor_readings.py
├── ai/
│   └── gemini_health_prompt.py
└── api/
    └── main.py
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Project info and health check |
| POST | /analyze | Analyze real sensor data |
| GET | /mock-analyze/{scenario} | Analyze a mock scenario |
| GET | /scenarios | List all available scenarios |
| GET | /trees | List monitored trees |

Available Scenarios: healthy, drought_stress, overwatering, pest_infestation, nutrient_deficiency

---

## 🗺️ Roadmap

- [x] Mock sensor data simulation
- [x] Gemini AI prompt integration
- [x] FastAPI REST backend
- [ ] Real IoT sensor integration (Raspberry Pi / Arduino)
- [ ] React.js dashboard with live charts
- [ ] SMS/Email alert system
- [ ] Multi-tree monitoring network
- [ ] Historical data logging

---

## 📄 License

MIT License

---

## 👤 Author

**Avinash Budige** - [@Avinashbudige](https://github.com/Avinashbudige)

> "The best time to plant a tree was 20 years ago. The second best time is now — and to listen to it."