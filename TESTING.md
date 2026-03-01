# 🧪 Testing Guide - Smoke Tests & Live Tests

TreeTalk AI includes two types of automated tests:

1. **Smoke Tests** - Quick sanity checks (no external dependencies)
2. **Live Tests** - Real API endpoint validation

---

## 📋 Quick Start

### Smoke Tests (Run Anytime)
```bash
# No dependencies, just tests the core code
python smoke_test.py

# Expected output: ✅ ALL SMOKE TESTS PASSED
```

### Live Tests (Requires Running API)
```bash
# Terminal 1: Start the API
python -m uvicorn api.main:app --reload

# Terminal 2: Run live tests against the API
python live_test.py

# Expected output: ✅ ALL LIVE TESTS PASSED
```

---

## 🔥 Smoke Test - Fast & Lightweight

### What It Tests (No API Required)

**Test Group 1: Critical Imports**
- Import all core modules
- Verify dependencies are installed
- Check module structure

**Test Group 2: File Structure**
- Verify all required files exist
- Check project structure integrity
- Ensure configuration files present

**Test Group 3: Prompt System**
- System prompt generation
- Analysis prompt generation
- Quick reference guide generation

**Test Group 4: Sensor Data**
- All 5 scenarios available
- Data generation for each scenario
- Optimal ranges defined

**Test Group 5: API Models**
- SensorData validation (valid data)
- HealthReport validation
- Invalid data rejection

**Test Group 6: Integration**
- TreeHealthMonitor initialization
- Sensor simulation
- Report handling methods

### Running Smoke Tests

```bash
python smoke_test.py
```

### Expected Output
```
============================================================
  TreeTalk AI - Smoke Test Suite
============================================================

============================================================
  Test 1: Critical Imports
============================================================

✅ PASS: Import ai.gemini_health_prompt
✅ PASS: Import api.main
✅ PASS: Import sensors.mock_sensor_readings
✅ PASS: Import example_integration

... (more tests)

============================================================
  Smoke Test Summary
============================================================

Results:
  Passed: 24
  Failed: 0
  Total:  24
  Pass Rate: 100.0%

✅ ALL SMOKE TESTS PASSED!
   TreeTalk AI MVP is HEALTHY and ready to use! 🌳
```

### Exit Codes
- **0** = All tests passed ✅
- **1** = Some tests failed ❌

---

## 🌐 Live Tests - Full API Validation

### What It Tests (Requires Running API)

**Test Group 1: API Endpoints**
- Verify all 4 endpoints respond
- Check HTTP status codes
- Validate response formats

**Test Group 2: Health Check**
- GET / endpoint
- Project info response
- Version information

**Test Group 3: Scenarios**
- All 5 scenarios available
- Scenario list endpoint
- Response validation

**Test Group 4: Mock Analysis**
- Mock data generation
- Response structure validation
- Severity classification
- Analysis completeness

**Test Group 5: Real Analysis**
- Sensor data acceptance
- Full analysis generation
- Response validation
- Gemini integration check

**Test Group 6: Error Handling**
- Invalid scenario rejection (HTTP 400)
- Missing field validation (HTTP 422)
- Proper error messages

**Test Group 7: Response Validation**
- Required fields present
- Correct field types
- JSON serialization validity
- Content completeness

### Running Live Tests

#### Step 1: Start the API
```bash
python -m uvicorn api.main:app --reload

# Output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# ✅ Gemini AI connection verified
```

#### Step 2: Run Live Tests (in another terminal)
```bash
python live_test.py
```

### Expected Output
```
======================================================================
  TreeTalk AI - Live API Test Suite
======================================================================

ℹ️  Make sure API is running:
  python -m uvicorn api.main:app --reload

======================================================================
  Test 1: API Endpoints
======================================================================

✅ PASS: GET /
       Health check - HTTP 200
✅ PASS: GET /scenarios
       List scenarios - HTTP 200
✅ PASS: GET /mock-analyze/healthy
       Mock analysis - HTTP 200
✅ PASS: POST /analyze
       Real analysis - HTTP 200

... (more tests)

======================================================================
  Live Test Summary
======================================================================

Results:
  Passed: 27
  Failed: 0
  Total:  27
  Pass Rate: 100.0%

✅ ALL LIVE TESTS PASSED!
   API is working correctly and ready for production! 🚀
```

### Exit Codes
- **0** = All tests passed ✅
- **1** = Some tests failed ❌

---

## 📊 Test Comparison

| Feature | Smoke Test | Live Test |
|---------|-----------|-----------|
| **No API Required** | ✅ | ❌ |
| **Test Duration** | ~2-5 sec | ~10-30 sec |
| **Tests Core Code** | ✅ | ✅ |
| **Tests API Endpoints** | ❌ | ✅ |
| **Tests Gemini Integration** | ❌ | ✅ |
| **Error Handling** | ❌ | ✅ |
| **Response Validation** | ❌ | ✅ |
| **Best For** | Quick pre-commit | Pre-deployment |

---

## 🔄 CI/CD Integration

### GitHub Actions Workflow
Both tests run automatically via GitHub Actions:

```yaml
# .github/workflows/tests.yml
- Run pytest
- Run smoke_test.py
- Run live tests (with mocked API)
```

### Manual CI Testing
```bash
# Run all tests locally (simulating CI)
pytest tests/ -v
python smoke_test.py
python live_test.py  # With running API
```

---

## 🎯 Testing Workflow

### For Developers

1. **Before committing:**
   ```bash
   python smoke_test.py  # Quick check
   ```

2. **Before pushing to main:**
   ```bash
   pytest tests/ -v
   python smoke_test.py
   # Start API, then:
   python live_test.py
   ```

### For CI/CD

1. **Every push/PR:**
   - Run smoke_test.py ✅
   - Run pytest ✅
   - Run live_test.py (with mock API) ✅

2. **Pre-deployment:**
   - Run all tests
   - Verify live_test.py passes
   - Check security scans

---

## 🛠️ Customizing Tests

### Adding a New Smoke Test

Edit `smoke_test.py`:
```python
def test_my_feature(self):
    """Test description."""
    print_header("Test X: My Feature")
    
    try:
        # Your test code here
        assert condition, "Assertion message"
        print_pass("Test name", "Details")
        self.passed += 1
    except Exception as e:
        print_fail("Test name", str(e))
        self.failed += 1
```

### Adding a New Live Test

Edit `live_test.py`:
```python
def test_my_endpoint(self):
    """Test API endpoint."""
    print_header("Test X: My Endpoint")
    
    try:
        response = self.client.get(f"{self.api_url}/my-endpoint")
        assert response.status_code == 200
        data = response.json()
        # Validate response
        print_pass("Endpoint test", "Details")
        self.passed += 1
    except Exception as e:
        print_fail("Endpoint test", str(e))
        self.failed += 1
```

---

## 📈 Test Metrics

### Current Coverage

```
Smoke Tests:      24 tests
Live Tests:       27 tests (7 test groups)
Code Paths:       50+ code paths tested
Scenarios:        5 scenarios validated
Endpoints:        4 endpoints validated
Error Cases:      5+ error cases tested
```

### Test Execution Times

```
Smoke Tests:      ~2-5 seconds
Live Tests:       ~10-30 seconds (depends on Gemini API)
Full Suite:       ~30-60 seconds
```

---

## 🆘 Troubleshooting

### Smoke Test Failures

**Import Error**
```bash
# Fix: Install dependencies
pip install -r requirements.txt
```

**File Not Found**
```bash
# Fix: Run from project root directory
cd /workspaces/treetalk-ai
python smoke_test.py
```

### Live Test Failures

**Cannot Connect to API**
```bash
# Fix: Start the API first
python -m uvicorn api.main:app --reload
```

**Timeout on Analysis**
```bash
# Gemini API is slow
# Solution: Increase timeout in live_test.py
self.timeout = 60.0  # Increase from 30
```

**HTTP 422 - Validation Error**
```bash
# Invalid sensor data
# Fix: Check sensor_data format in live_test.py
```

---

## 📝 Test Output Guide

### Color Coding
```
✅ GREEN = Test passed
❌ RED = Test failed
ℹ️ CYAN = Information message
⚠️ YELLOW = Warning
```

### Status Indicators
```
✅ PASS  = Test succeeded
❌ FAIL  = Test failed (see reason)
→ Arrow = Error detail
```

---

## 🎓 Best Practices

### Before Each Commit
```bash
python smoke_test.py
```

### Before Pushing Code
```bash
pytest tests/ -v
python smoke_test.py
```

### Before Deploying
```bash
pytest tests/ -v
python smoke_test.py
python -m uvicorn api.main:app --reload &
python live_test.py
kill %1  # Stop API
```

### Before Releasing
```bash
# Full test suite
pytest tests/ -v
python smoke_test.py
python live_test.py
python test_mvp.py
```

---

## 📚 Related Files

- `smoke_test.py` - Smoke test suite
- `live_test.py` - Live API tests
- `test_mvp.py` - MVP test suite
- `tests/` - Pytest test directory
- `.github/workflows/tests.yml` - CI/CD integration

---

## 🚀 Quick Commands

```bash
# Run all smoke tests
python smoke_test.py

# Run all live tests (API must be running)
python live_test.py

# Run both with API
python -m uvicorn api.main:app --reload &
python smoke_test.py && python live_test.py
kill %1

# Run pytest suite
pytest tests/ -v

# Run MVP test suite
python test_mvp.py

# Full validation (all tests)
pytest tests/ -v && python smoke_test.py && python test_mvp.py
```

---

## ✅ Testing Checklist

Before production:
- [ ] Smoke tests pass
- [ ] Pytest tests pass
- [ ] MVP tests pass
- [ ] Live tests pass
- [ ] Security scan passes
- [ ] No linting errors
- [ ] Documentation is current

Before release:
- [ ] All tests passing on main branch
- [ ] All tests passing on Python 3.9-3.12
- [ ] Live tests with real Gemini API
- [ ] Manual testing of key features
- [ ] Security review completed

---

**"Give trees a voice before it's too late."** 🌳

For more information, see:
- [README.md](README.md) - Project overview
- [CI-CD.md](CI-CD.md) - CI/CD documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
