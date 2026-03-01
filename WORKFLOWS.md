# GitHub Actions Workflows

This project includes 7 comprehensive GitHub Actions workflows that provide automated testing, security scanning, documentation validation, and deployment capabilities.

## Workflow Overview

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Core Tests** | `tests.yml` | Push/PR | Python 3.9-3.12 matrix testing |
| **API Health** | `api-health.yml` | Daily (2 AM UTC) | API endpoint validation |
| **MVP Validation** | `mvp-tests.yml` | Push/PR | Comprehensive MVP testing |
| **Live Integration** | `live-tests.yml` | Push/PR | Real API endpoint tests |
| **Security** | `security.yml` | Push/Weekly | Bandit, Safety, credential scanning |
| **Documentation** | `docs.yml` | Push/PR | Markdown validation, link checking |
| **Deploy** | `deploy.yml` | Release | Release notes, deployment checks |

---

## 1. Core Tests Workflow (`tests.yml`)

**Purpose:** Validate code functionality across Python versions

**Triggers:**
- On push to `main` or `develop` branches
- On pull requests to `main` or `develop` branches

**Matrix:** Python 3.9, 3.10, 3.11, 3.12

**Jobs:**
- **test** (4 Python versions):
  - Install pygame (sensor reading simulation)
  - Run pytest with coverage reporting
  - Execute all project tests
  - Upload coverage to Codecov

**Expected Duration:** 3-5 minutes per Python version

**Key Validations:**
- ✅ All imports work across Python versions
- ✅ Sensor data generation functions properly
- ✅ Prompt system generates valid output
- ✅ API models validate correctly

---

## 2. API Health Workflow (`api-health.yml`)

**Purpose:** Ensure API endpoints remain healthy and accessible

**Triggers:**
- Scheduled daily at 2:00 AM UTC
- Can be manually triggered via workflow dispatch
- Scheduled weekly during maintenance windows

**Jobs:**
- **api-health-check**:
  - Start FastAPI server with test credentials
  - Verify API responds (HTTP 200 on GET /)
  - Validate endpoint structure
  - Check critical imports
  - Test data model validation
  - Stop server gracefully

**Expected Duration:** 2-3 minutes

**Checks Performed:**
- ✅ Server startup completes without errors
- ✅ GET / endpoint returns health status
- ✅ Health check includes version and endpoints
- ✅ Pydantic models validate correctly
- ✅ Error handling works (invalid input rejected)

**Alert Conditions:**
- ❌ Server fails to start
- ❌ Health check endpoint returns error
- ❌ Import errors detected
- ❌ Data validation fails

---

## 3. MVP Validation Workflow (`mvp-tests.yml`)

**Purpose:** Comprehensive validation of all MVP components

**Triggers:**
- On push to `main` or `develop` branches
- On pull requests to `main` or `develop` branches

**Jobs:**

### 3.1 Smoke Tests Job
- **Purpose:** Fast sanity checks (2-5 seconds)
- **Tests:** 24+ tests across 6 categories
- **Coverage:**
  - Critical imports (fastapi, pydantic, google.generativeai)
  - File structure (all required files exist)
  - Prompt system (system/analysis/quick-ref prompts generated)
  - Sensor data (all 5 scenarios available, 14 parameters)
  - API models (SensorData/HealthReport validation)
  - Integration (TreeHealthMonitor class functions)
- **Exit Code:** 0=success, 1=failure

### 3.2 MVP Validation Job
- **Purpose:** Complete MVP feature testing
- **Tests:** 6 validation categories
- **Coverage:**
  - Imports validation
  - File structure verification
  - Prompt system testing
  - Sensor data simulation
  - API model validation
  - Integration testing

**Expected Duration:** 2-3 minutes total

**Key Validations:**
- ✅ All 5 test scenarios generate valid data
- ✅ Sensor parameters within expected ranges
- ✅ Prompts generate comprehensive analysis (>500 chars)
- ✅ API models handle valid and invalid input
- ✅ Error cases return proper HTTP status codes

---

## 4. Live Integration Workflow (`live-tests.yml`)

**Purpose:** Real API endpoint testing with HTTP requests

**Triggers:**
- On push to `main` or `develop` branches
- On pull requests to `main` or `develop` branches

**Jobs:**

### 4.1 Live Tests Job
- **Purpose:** Test real HTTP endpoints (10-30 seconds)
- **Setup:**
  - Install Python 3.11
  - Install dependencies from requirements.txt
  - Create test .env file with dummy API key
  - Start Uvicorn API server in background
  - Wait for server to become healthy (max 30 seconds)
- **Tests:** 27+ tests across 7 categories
- **Coverage:**
  - Endpoint existence (GET /, GET /scenarios, GET /mock, POST /analyze)
  - Health check response structure
  - Scenarios list format and content
  - Mock analysis for all 5 scenarios
  - Real analysis request handling
  - Error handling (invalid scenario, missing fields)
  - Response schema validation
- **Exit Code:** 0=success, 1=failure
- **Cleanup:** Kill API server after tests complete

### 4.2 Smoke Tests Job
- **Purpose:** Fast component validation (2-5 seconds)
- **Runs in parallel with live tests** for faster feedback
- **Tests:** 24+ tests (same as MVP workflow)

**Expected Duration:** 10-30 seconds (live tests), 2-5 seconds (smoke tests)

**Endpoints Tested:**
| Method | Endpoint | Test Cases |
|--------|----------|-----------|
| GET | `/` | Response contains status, version, endpoints |
| GET | `/scenarios` | Returns list of 5 scenarios with proper names |
| GET | `/mock-analyze/{scenario}` | Valid scenario returns analysis; invalid returns 400 |
| POST | `/analyze` | Valid sensor data analyzed; invalid returns 422 |

**Response Schema Validation:**
```json
{
  "tree_name": "string",
  "timestamp": "ISO 8601 datetime",
  "health_status": "HEALTHY|CAUTION|WARNING|CRITICAL",
  "analysis": "multi-part analysis text (>500 chars)",
  "severity": 1-4 (1=HEALTHY, 2=CAUTION, 3=WARNING, 4=CRITICAL)
}
```

---

## 5. Security Workflow (`security.yml`)

**Purpose:** Identify security vulnerabilities and code quality issues

**Triggers:**
- On push to `main` or `develop` branches
- On pull requests
- Weekly schedule (every Monday at midnight UTC)

**Jobs:**
- **security-scan**:
  - Bandit: Python security issue scanning
  - Safety: Dependency vulnerability checking
  - Flake8: Code style and quality
  - Black: Code formatting check
  - isort: Import statement sorting
  - Trufflewhore: Secrets/credentials detection

**Expected Duration:** 2-3 minutes

**Checks Performed:**
- ✅ No hardcoded secrets (API keys, passwords)
- ✅ No SQL injection vulnerabilities
- ✅ No insecure password hashing
- ✅ All dependencies are up-to-date
- ✅ Code follows PEP 8 style guidelines
- ✅ Import statements properly sorted

**Alert Conditions:**
- ❌ High-severity security issues
- ❌ Vulnerable dependencies
- ❌ Detected secrets
- ❌ Code quality failures

---

## 6. Documentation Workflow (`docs.yml`)

**Purpose:** Validate documentation quality and integrity

**Triggers:**
- On push to `main` or `develop` branches
- On pull requests affecting documentation

**Jobs:**
- **docs-validation**:
  - Check Markdown syntax
  - Validate links (internal and external)
  - Verify README structure
  - Check for broken references

**Expected Duration:** 1-2 minutes

**Validations:**
- ✅ All Markdown files have valid syntax
- ✅ Internal links point to existing files
- ✅ External links are resolvable
- ✅ README contains required sections
- ✅ Code examples are properly formatted

---

## 7. Deploy Workflow (`deploy.yml`)

**Purpose:** Prepare and validate releases for deployment

**Triggers:**
- On release creation explicitly
- Manual trigger via workflow dispatch

**Jobs:**
- **validate-release**:
  - Run all tests (smoke, live, security)
  - Generate release notes
  - Validate version numbers
  - Check changelog entries

- **prepare-deployment**:
  - Create deployment artifacts
  - Generate deployment checklist
  - Prepare container images (if applicable)

**Expected Duration:** 5-10 minutes

**Pre-Deployment Checks:**
- ✅ All tests pass
- ✅ Security scan clean
- ✅ Documentation updated
- ✅ Version bumped appropriately
- ✅ Changelog entry present
- ✅ Release notes generated

---

## Workflow Execution Order

### On Push to main/develop:
1. **Parallel Execution (immediate):**
   - `tests.yml` - Core tests (matrix: 4 Python versions)
   - `mvp-tests.yml` - MVP validation (contains smoke tests)
   - `live-tests.yml` - Live integration tests
   - `security.yml` - Security scanning
   - `docs.yml` - Documentation validation

2. **Sequential (after parallel complete):**
   - Deploy workflow can be triggered manually

### Scheduled Executions:
- **Daily:** API health check at 2 AM UTC
- **Weekly:** Security scan and dependency audit

---

## Status Badges

Add these badges to your README to display workflow status:

```markdown
![Tests](https://github.com/your-org/treetalk-ai/actions/workflows/tests.yml/badge.svg)
![API Health](https://github.com/your-org/treetalk-ai/actions/workflows/api-health.yml/badge.svg)
![MVP Tests](https://github.com/your-org/treetalk-ai/actions/workflows/mvp-tests.yml/badge.svg)
![Live Tests](https://github.com/your-org/treetalk-ai/actions/workflows/live-tests.yml/badge.svg)
![Security](https://github.com/your-org/treetalk-ai/actions/workflows/security.yml/badge.svg)
![Docs](https://github.com/your-org/treetalk-ai/actions/workflows/docs.yml/badge.svg)
```

---

## Local Workflow Testing

### Test locally before pushing:

```bash
# Run all smoke tests (no dependencies)
python smoke_test.py

# Start API and run live tests
python -m uvicorn api.main:app &
sleep 2  # Wait for server
python live_test.py
pkill -f uvicorn  # Stop server

# Run security checks locally
pip install bandit safety flake8 black isort
bandit -r . --skip B101,B601
safety check
flake8 . --max-line-length=100
black --check .
isort --check-only .
```

---

## Debugging Workflow Failures

### Common Issues and Solutions:

**Issue: Tests timeout in CI**
```yaml
# Solution: Increase timeout in workflow
timeout-minutes: 10  # Increase from 5
```

**Issue: API fails to start**
```yaml
# Solution: Increase wait time for server startup
max_attempts=60  # Increase from 30
sleep 1  # Already at 1 second
```

**Issue: Gemini API calls fail**
```bash
# Solution: Use test key in CI
GEMINI_API_KEY=test_key_for_ci

# For real testing, set in GitHub Secrets:
# Settings > Secrets and variables > Actions > New repository secret
```

**Issue: Port already in use**
```bash
# Solution: Kill existing process
pkill -f "uvicorn api.main:app"
```

---

## GitHub Actions Configuration

### Repository Secrets Required:
```
GEMINI_API_KEY        - Your actual API key for deployment
GITHUB_TOKEN          - Auto-generated, used for releases
```

### Environment Variables Used:
- `GEMINI_API_KEY` - Set to test_key_for_ci in CI environments
- `SERVER_HOST` - Set to 0.0.0.0 in CI
- `SERVER_PORT` - Set to 8000 in CI

### Required Repository Settings:
1. Enable GitHub Actions
2. Allow read and write permissions for GitHub Actions
3. Add required secrets (GEMINI_API_KEY for deployment)
4. Configure branch protection rules if desired

---

## Performance Metrics

**Typical Workflow Runtimes:**
- Tests (Python 3.11): 90-120 seconds
- API Health: 120-180 seconds
- MVP Tests: 60-90 seconds (with smoke + full validation)
- Live Tests: 30-60 seconds (depends on API startup)
- Security: 120-180 seconds
- Docs: 30-60 seconds
- **Total for all workflows:** ~5-8 minutes (parallel execution)

**Optimization Tips:**
1. Use `workflow_run` to trigger dependent workflows
2. Enable workflow caching with `actions/setup-python@v4`
3. Use matrix strategy for split testing
4. Run long-duration tests in parallel jobs

---

## Next Steps

1. **Customize workflows for your environment**
   - Update repository references
   - Add your org/repo to badge URLs
   - Configure branch names if different

2. **Set up GitHub Secrets**
   - Add GEMINI_API_KEY for production deployments
   - Configure deployment credentials if needed

3. **Monitor workflow runs**
   - Check Actions tab for real-time status
   - Review logs for any failures
   - Set up notifications for failures

4. **Extend workflows as needed**
   - Add Docker build jobs
   - Add deployment to cloud platforms
   - Add automated version bumping

See [CI-CD.md](CI-CD.md) and [GITHUB-ACTIONS.md](GITHUB-ACTIONS.md) for additional information.
