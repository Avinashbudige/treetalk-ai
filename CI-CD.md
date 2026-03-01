# 🔄 CI/CD Pipeline Documentation

## Overview

TreeTalk AI uses **GitHub Actions** to automate testing, validation, and deployment. This ensures code quality and system reliability with every push and pull request.

---

## 🎯 Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions Workflows                   │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│  On Push / Pull Request  │
└──────────┬───────────────┘
           │
           ├─→ tests.yml (Parallel)
           │   ├─ Pytest on Python 3.9-3.12
           │   ├─ Mock sensor validation
           │   ├─ Prompt system testing
           │   └─ Code linting (flake8, black, isort)
           │
           ├─→ api-health.yml (Parallel)
           │   ├─ API startup verification
           │   ├─ Endpoint structure validation
           │   ├─ Data model validation
           │   └─ Critical imports check
           │
           ├─→ mvp-tests.yml (Parallel)
           │   ├─ Prompt system test
           │   ├─ Sensor data generation
           │   ├─ API models validation
           │   ├─ Data consistency
           │   ├─ Integration example
           │   └─ File integrity
           │
           ├─→ security.yml (Parallel)
           │   ├─ Dependency check
           │   ├─ Security scanning (bandit)
           │   ├─ Vulnerability scanning (safety)
           │   └─ Hardcoded secrets detection
           │
           └─→ docs.yml (Parallel)
               ├─ Markdown validation
               ├─ Broken link detection
               └─ Documentation structure check

┌──────────────────────────┐
│  On Release Tag (v*.*)   │
└──────────┬───────────────┘
           │
           └─→ deploy.yml
               ├─ Generate release notes
               ├─ Run pre-deployment checks
               ├─ Validate configuration
               └─ Generate deployment manifest
```

---

## 📋 Workflows Definition

### 1. **tests.yml** — Core Test Suite
**Runs on:** Push to main/develop, Pull Requests

**What it does:**
- Tests on Python 3.9, 3.10, 3.11, 3.12 (matrix strategy)
- Runs pytest on all test files
- Validates mock sensor data generation
- Verifies API can start
- Tests prompt system completeness
- Validates sensor data format
- Tests Pydantic models

**Key steps:**
```yaml
- Run pytest across versions
- Test sensor data generation
- Verify API startup
- Validate prompt system
- Validate sensor data format
- Run linting (flake8, black, isort)
```

**Status:** ✅ Runs on every push/PR

---

### 2. **api-health.yml** — API Validation
**Runs on:** Push to main/develop, Pull Requests, Daily schedule (2 AM UTC)

**What it does:**
- Verifies API structure and integrity
- Checks all endpoints are properly configured
- Validates data models (SensorData, HealthReport)
- Tests critical imports
- Verifies scenario data availability
- Checks prompt system compliance

**Key tests:**
- FastAPI app routes (4 endpoints validated)
- SensorData & HealthReport Pydantic models
- Mock scenario availability (5 scenarios)
- System prompt structure

**Status:** ✅ Daily automated + on-demand validation

---

### 3. **mvp-tests.yml** — Comprehensive MVP Validation
**Runs on:** Push to main/develop, Pull Requests

**What it does:**
A 6-test comprehensive validation:

1. **Prompt System Test**
   - System prompt generation (>200 chars)
   - Analysis prompt generation with tree data
   - Quick reference guide completeness

2. **Sensor Data Generation Test**
   - All scenarios generate valid data
   - All 14 required fields present
   - Data value ranges are reasonable

3. **API Models Test**
   - Valid SensorData validation
   - HealthReport model validation
   - Invalid data rejection

4. **Data Consistency Test**
   - Optimal ranges defined
   - Scenario ranges valid (min < max)

5. **Integration Example Test**
   - TreeHealthMonitor initialization
   - Simulator data generation
   - Report handling methods

6. **File Integrity Test**
   - All required files present
   - Documentation files valid

**Output:** Color-coded summary (✅ all pass or ❌ details failures)

---

### 4. **security.yml** — Security & Dependencies
**Runs on:** Push to main/develop, Pull Requests, Weekly (Monday 2 AM UTC)

**Jobs:**
- **dependencies** - Check installed packages, verify versions
- **security** - Bandit scan, Safety vulnerability check, secrets detection
- **requirements** - Validate requirements.txt, check for duplicates

**Tools used:**
- `bandit` - Find common security issues
- `safety` - Check for known vulnerabilities
- `pip list` - Verify package integrity

**Status:** ✅ Production security checks

---

### 5. **docs.yml** — Documentation Validation
**Runs on:** Documentation changes, README updates

**What it does:**
- Validates all markdown files exist and are non-empty
- Checks for broken file references
- Verifies README contains required sections
- Generates project summary
- Calculates code metrics
- Verifies workflow files

**Required sections in README:**
- TreeTalk AI
- Why TreeTalk AI
- Architecture
- Sensors Used
- Quick Start
- Installation
- Project Structure
- API Endpoints
- Roadmap
- License

---

### 6. **deploy.yml** — Release & Deployment
**Runs on:** Version tags (v*.*), Manual dispatch

**Jobs:**
- **release-notes** - Generate release notes template
- **pre-deployment** - Run full test suite before deployment

**Pre-deployment checks:**
- Import all critical modules
- Validate configuration
- Verify API structure
- Generate deployment manifest

**Status:** ✅ On-demand release process

---

## 🔄 Workflow Triggers

### Automatic Triggers
| Trigger | Workflows |
|---------|-----------|
| Push to `main` | All except deploy |
| Push to `develop` | All except deploy |
| Pull Request to `main` | All except deploy |
| PR changes to .md | docs.yml only |
| Daily (2 AM UTC) | api-health.yml |
| Weekly (Mon 2 AM) | security.yml |
| Version tag (v*) | deploy.yml |

### Manual Triggers
All workflows can be triggered manually via GitHub UI:
- Go to: Actions → Choose workflow → "Run workflow"

---

## 📊 Test Coverage

### Unit Tests
- **Prompt System** - System prompt, analysis prompt generation
- **Sensor Data** - All 5 scenarios, range validation
- **API Models** - Input/output validation
- **Integration** - TreeHealthMonitor functionality

### Integration Tests
- **API Startup** - Verify FastAPI app initialization
- **Data Flow** - Sensor → Prompt → Response
- **Model Validation** - Pydantic schema compliance

### Security Tests
- **Dependencies** - Version pinning, vulnerability scanning
- **Code Quality** - Linting, formatting, complexity
- **Secrets** - Hardcoded credentials detection

### Documentation Tests
- **Markdown** - Syntax validation, link checking
- **Structure** - Required sections, file integrity
- **Examples** - Code examples validity

---

## 🎨 Badge Status

Add these badges to your documentation:

```markdown
[![Tests & API Validation](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/tests.yml)
[![API Health Check](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/api-health.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/api-health.yml)
[![MVP Test Suite](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/mvp-tests.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/mvp-tests.yml)
[![Security & Dependencies](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/security.yml/badge.svg)](https://github.com/Avinashbudige/treetalk-ai/actions/workflows/security.yml)
```

---

## 🔧 Local Workflow Simulation

### Run Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-asyncio flake8 black isort bandit safety

# Run pytest
pytest tests/ -v

# Run linting
flake8 ai/ api/ sensors/ tests/
black --check ai/ api/ sensors/

# Run security checks
bandit -r ai/ api/ sensors/
safety check

# Run MVP tests
python test_mvp.py
```

### Validate Workflows Locally

You can use `act` to run GitHub Actions workflows locally:

```bash
# Install act: https://github.com/nektos/act
act push -j test

# Or run specific workflow
act -l  # List all workflows
```

---

## 📈 Performance Metrics

### Typical Execution Times

| Workflow | Duration |
|----------|----------|
| tests.yml | 3-5 min |
| api-health.yml | 2-3 min |
| mvp-tests.yml | 2-3 min |
| security.yml | 2-4 min |
| docs.yml | 1-2 min |
| **Total (parallel)** | ~5-6 min |

---

## ✅ Checklist for Maintainers

When maintaining the project, ensure:

- [ ] All workflows are passing
- [ ] Tests pass on all Python versions (3.9-3.12)
- [ ] No security vulnerabilities detected
- [ ] Documentation is up-to-date
- [ ] No broken references in README
- [ ] Code follows style guidelines (flake8, black)
- [ ] Dependencies are pinned to specific versions
- [ ] API endpoints are documented

---

## 🚀 Continuous Integration Best Practices

### For Contributors

1. **Make sure CI passes** before requesting review
2. **Test locally** before pushing:
   ```bash
   pytest tests/ -v
   python test_mvp.py
   ```
3. **Follow code style**:
   ```bash
   black ai/ api/
   flake8 ai/ api/
   ```
4. **Update documentation** if adding features

### For Maintainers

1. **Monitor workflow logs** for failures
2. **Keep dependencies updated** (weekly check)
3. **Review security alerts** immediately
4. **Tag releases properly** (v0.1.0 format)
5. **Generate release notes** on version tag

---

## 🆘 Troubleshooting

### Workflow Failures

**Tests failing:**
- Check Python version compatibility (3.9-3.12)
- Review test error logs
- Run locally: `pytest tests/ -v`

**API health check failing:**
- Verify .env configuration
- Check API imports
- Ensure all endpoints defined

**Security warnings:**
- Review bandit report
- Update vulnerable dependencies
- Check for hardcoded secrets

**Documentation checks failing:**
- Verify all markdown files exist
- Check for broken links
- Run locally: `python -c "import markdown"`

---

## 📞 Support

For CI/CD issues:
1. Check workflow logs: GitHub Actions → Workflow → Logs
2. Review workflow file: `.github/workflows/*.yml`
3. Run tests locally to debug
4. Open an issue with error details

---

## 📚 Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Workflow Syntax:** https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- **Act (local runner):** https://github.com/nektos/act
- **Pytest:** https://docs.pytest.org
- **Flake8:** https://flake8.pycqa.org

---

**"Give trees a voice before it's too late."** 🌳

Maintained with ❤️ and automated with 🤖 GitHub Actions
