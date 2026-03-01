# 🌳 TreeTalk AI

> **"Give trees a voice before it's too late."**

[![Tests & API Validation](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/tests.yml)
[![API Health Check](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/api-health.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/api-health.yml)
[![MVP Test Suite](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/mvp-tests.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/mvp-tests.yml)
[![Live API Tests](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/live-tests.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/live-tests.yml)
[![Security & Dependencies](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/security.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/security.yml)

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

## 🧪 Testing

TreeTalk AI includes comprehensive automated tests:

### Smoke Tests (Quick Checks)
```bash
python smoke_test.py
```
- ✅ Runs in 2-5 seconds
- ✅ No external dependencies
- ✅ Validates all core components
- ✅ 24+ tests

### Live Tests (Full API Validation)
```bash
# Terminal 1: Start API
python -m uvicorn api.main:app --reload

# Terminal 2: Run live tests
python live_test.py
```
- ✅ Tests real API endpoints
- ✅ Validates responses
- ✅ Checks error handling
- ✅ 27+ tests

For detailed testing guide, see [TESTING.md](TESTING.md) and [SMOKE-LIVE-TESTS.md](SMOKE-LIVE-TESTS.md)

---

## 📁 Project Structure

```
treetalk-ai/
├── README.md
├── DOCUMENTATION.md              ← Start here for all docs
├── requirements.txt
├── .env.example
├── .gitignore
├── sensors/
│   └── mock_sensor_readings.py
├── ai/
│   └── gemini_health_prompt.py
├── api/
│   └── main.py
├── tests/
│   └── test_api.py
├── smoke_test.py                 ← Fast validation (2-5s)
├── live_test.py                  ← Full API tests (10-30s)
└── .github/
    └── workflows/                ← 7 CI/CD workflows
```

### Documentation Files

See [DOCUMENTATION.md](DOCUMENTATION.md) for complete documentation index with reading paths for different roles.

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

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for automated testing, validation, and deployment.

### Automated Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| **Tests & API Validation** | Run pytest across Python 3.9-3.12 | Push/PR |
| **API Health Check** | Verify API startup, endpoints, data models | Daily + On-demand |
| **MVP Test Suite** | Comprehensive MVP validation with smoke tests | Push/PR |
| **Live API Tests** | Real HTTP endpoint validation | Push/PR |
| **Security & Dependencies** | Code security, vulnerability scanning | Push/PR + Weekly |
| **Documentation** | Markdown validation, link checking | Documentation changes |
| **Release & Deployment** | Pre-deployment checks and release notes | Version tags |

### View Status & Details

- [GitHub Actions](https://github.com/Avinashbudige/treetalk-ai/actions) - Real-time workflow status
- [WORKFLOWS.md](WORKFLOWS.md) - Complete workflow documentation
- [CI-CD.md](CI-CD.md) - CI/CD configuration guide
- [Workflow Directory](.github/workflows/) - All workflow definitions

### Local Testing

To run the same tests locally:

```bash
# Fast smoke tests (2-5 seconds, no dependencies)
python smoke_test.py

# Live API tests (requires running API server)
python -m uvicorn api.main:app &
sleep 2
python live_test.py
pkill -f uvicorn

# Run pytest suite
pytest tests/ -v

# Run MVP test suite
python test_mvp.py

# Run security checks
flake8 ai/ api/ sensors/ tests/
bandit -r ai/ api/ sensors/
```

See [TESTING.md](TESTING.md) for detailed testing instructions.

---
## 📖 Learn More

| Want to... | Start with... |
|-----------|---------|
| Get up and running | [QUICKSTART.md](QUICKSTART.md) - 5 minute setup |
| Understand architecture | [OVERVIEW.md](OVERVIEW.md) - System design |
| See all documentation | [DOCUMENTATION.md](DOCUMENTATION.md) - Complete index |
| Test the system | [TESTING.md](TESTING.md) - Testing guide |
| Deploy to production | [CI-CD-QUICK-REF.md](CI-CD-QUICK-REF.md) - Quick commands |
| Integrate sensors | [example_integration.py](example_integration.py) - Sensor examples |

---
## �🗺️ Roadmap

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