# Documentation Index

Complete guide to all documentation files in the TreeTalk AI project.

## 📚 Core Documentation

### [README.md](README.md)
**Start here!** Project overview, quick start guide, and main features.
- Project mission and why it matters
- Quick installation (3 commands)
- Architecture diagram
- Sensor specifications
- API endpoints overview
- CI/CD status badges

**Read if:** You're new to the project or need a quick overview

---

### [QUICKSTART.md](QUICKSTART.md)
**Get running in 5 minutes.** Step-by-step setup and first test.
- Complete installation walkthrough
- Environment configuration
- Running the first analysis
- Interpreting health reports
- Next steps for development

**Read if:** You want to get up and running quickly

---

## 🏗️ Architecture & Implementation

### [OVERVIEW.md](OVERVIEW.md)
**Understand the big picture.** Complete system design and data flow.
- TreeTalk AI vision and approach
- System architecture (3 layers)
- Data flow diagrams
- Health scoring algorithm
- Severity classification
- Safety considerations

**Read if:** You need to understand how the system works

---

### [IMPLEMENTATION.md](IMPLEMENTATION.md)
**Technical deep dive.** Code structure and implementation details.
- Project structure breakdown
- Module responsibilities
- Key algorithms
- Sensor data model
- 5 health scenarios (healthy, drought, overwatering, pest, nutrient)
- Code examples

**Read if:** You're contributing code or need technical details

---

### [MVP_SUMMARY.md](MVP_SUMMARY.md)
**MVP scope and features.** What's included and what's planned.
- MVP components (sensors, AI, API)
- 14 sensor parameters
- 5 test scenarios
- API endpoints (4 total)
- Pydantic validation models
- Severity levels (HEALTHY, CAUTION, WARNING, CRITICAL)

**Read if:** You need to understand MVP capabilities

---

## 🧪 Testing & Quality Assurance

### [TESTING.md](TESTING.md)
**Complete testing guide.** All testing approaches and strategies.
- **Smoke Tests:** Fast component validation (2-5 seconds)
  - 24+ tests across 6 categories
  - No external dependencies
  - Validates imports, files, prompts, sensors, models, integration
  
- **Live Tests:** Real API endpoint validation (10-30 seconds)
  - 27+ tests across 7 categories
  - HTTP request/response validation
  - All endpoints covered
  
- **MVP Tests:** Comprehensive feature testing
  - 6 validation categories
  - Integrated with GitHub Actions
  
- **Pytest:** Native Python testing
  - 50+ tests in tests/ directory
  - CI/CD integration

**Read if:** You want to run tests or understand testing strategy

---

### [SMOKE-LIVE-TESTS.md](SMOKE-LIVE-TESTS.md)
**Detailed test suite documentation.** Implementation details for smoke and live tests.
- Test architecture and design
- Exit codes and return values
- Usage examples
- Coverage summary (51 tests total)
- Integration with CI/CD
- Debugging guide

**Read if:** You're developing tests or need debugging help

---

## 🔄 CI/CD & Deployment

### [WORKFLOWS.md](WORKFLOWS.md)
**Complete workflow documentation.** All 7 GitHub Actions workflows explained.
- **7 Workflows:**
  - Core Tests (Python 3.9-3.12 matrix)
  - API Health (Daily scheduled checks)
  - MVP Validation (Comprehensive testing)
  - Live Integration (Real endpoint testing)
  - Security (Vulnerability scanning)
  - Documentation (Link and syntax validation)
  - Deploy (Release preparation)

- **Triggers:** Push, PR, schedule, manual
- **Status badges:** All workflows with GitHub badges
- **Local testing:** How to test locally
- **Debugging:** Common issues and solutions

**Read if:** You need to understand CI/CD or modify workflows

---

### [CI-CD.md](CI-CD.md)
**CI/CD configuration guide.** Setup, configuration, and best practices.
- GitHub Actions setup
- Repository secrets configuration
- Workflow customization
- Environment variables
- Performance optimization
- Troubleshooting

**Read if:** You're setting up CI/CD in a new repository

---

### [GITHUB-ACTIONS.md](GITHUB-ACTIONS.md)
**GitHub Actions reference.** Actions used and configuration examples.
- Setup Python action configuration
- Caching strategies
- Matrix testing setup
- Artifact handling
- Notification setup

**Read if:** You're configuring GitHub Actions workflow

---

### [CI-CD-QUICK-REF.md](CI-CD-QUICK-REF.md)
**Quick reference guide.** Commands, status checks, and troubleshooting.
- Quick commands (local tests, status checks)
- Status dashboard
- Environment setup
- Troubleshooting (6 common issues)
- Performance optimization
- Pre-commit checklist
- CI/CD flow diagram

**Read if:** You need quick answers or commands

---

## 🔧 Development Guides

### [example_integration.py](example_integration.py)
**Integration examples.** Real sensor integration templates.
- GPIO sensor reading (Raspberry Pi)
- CSV file reading
- API integration
- Simulator reading
- TreeHealthMonitor class example
- Report generation

**Read if:** You're integrating real sensors

---

## 📊 File Status & Purpose

| File | Type | Size | Purpose |
|------|------|------|---------|
| [sensor_data_model.md](sensor_data_model.md) | Doc | Small | 14-sensor specification |
| [smoke_test.py](smoke_test.py) | Test | 500+ lines | Fast component validation |
| [live_test.py](live_test.py) | Test | 500+ lines | HTTP endpoint validation |
| [test_mvp.py](test_mvp.py) | Test | 369 lines | MVP feature testing |
| [ai/gemini_health_prompt.py](ai/gemini_health_prompt.py) | Code | 162 lines | AI prompt system |
| [api/main.py](api/main.py) | Code | 254 lines | REST API backend |
| [sensors/mock_sensor_readings.py](sensors/mock_sensor_readings.py) | Code | ~80 lines | Mock sensor data |
| [.github/workflows/](github/workflows/) | Config | 7 files | CI/CD automation |
| [requirements.txt](requirements.txt) | Config | ~10 lines | Python dependencies |

---

## 🎯 Reading Paths

### For New Contributors
1. Start: [README.md](README.md) - Get overview
2. Then: [QUICKSTART.md](QUICKSTART.md) - Set up locally
3. Next: [TESTING.md](TESTING.md) - Run tests
4. Finally: [IMPLEMENTATION.md](IMPLEMENTATION.md) - Understand code

**Time:** ~30 minutes

---

### For Integration
1. Start: [QUICKSTART.md](QUICKSTART.md) - Basic setup
2. Then: [example_integration.py](example_integration.py) - Integration templates
3. Finally: [IMPLEMENTATION.md](IMPLEMENTATION.md) - Understand data model

**Time:** ~20 minutes

---

### For DevOps
1. Start: [CI-CD-QUICK-REF.md](CI-CD-QUICK-REF.md) - Quick overview
2. Then: [WORKFLOWS.md](WORKFLOWS.md) - Understand workflows
3. Then: [CI-CD.md](CI-CD.md) - Configure CI/CD
4. Finally: [GITHUB-ACTIONS.md](GITHUB-ACTIONS.md) - Action details

**Time:** ~45 minutes

---

### For Testing
1. Start: [TESTING.md](TESTING.md) - Testing overview
2. Then: [SMOKE-LIVE-TESTS.md](SMOKE-LIVE-TESTS.md) - Test details
3. Then: [CI-CD-QUICK-REF.md](CI-CD-QUICK-REF.md) - Quick commands

**Time:** ~25 minutes

---

### For Debugging
1. Quick: [CI-CD-QUICK-REF.md](CI-CD-QUICK-REF.md) - Troubleshooting section
2. Then: [WORKFLOWS.md](WORKFLOWS.md) - Workflow details
3. Run: [TESTING.md](TESTING.md) - Run tests to verify

**Time:** ~15 minutes

---

## 📱 Quick Links

### Run Tests
```bash
python smoke_test.py                    # Fast (2-5s)
python live_test.py                     # Full API (10-30s)
pytest tests/ -v                        # All tests
```

### Start API
```bash
python -m uvicorn api.main:app --reload
# Then: curl http://localhost:8000/
```

### View CI/CD
- [GitHub Actions](https://github.com/Avinashbudige/treetalk-ai/actions)
- [All Workflows](.github/workflows/)
- [Test Results](#) - Links in README badges

---

## 🤝 Contributing

1. Read: [README.md](README.md) - Understand project
2. Read: [IMPLEMENTATION.md](IMPLEMENTATION.md) - Code structure
3. Read: [TESTING.md](TESTING.md) - Test requirements
4. Run tests locally: All tests must pass
5. Submit PR with tests for changes

See [TESTING.md](TESTING.md#running-tests-locally) for detailed steps.

---

## 📋 Documentation Checklist

When updating documentation:
- [ ] Update relevant doc file
- [ ] Update [Documentation Index](DOCUMENTATION.md) if adding new file
- [ ] Run smoke tests to verify no code broke
- [ ] Update links in [README.md](README.md) if needed
- [ ] Check for broken links: `linkchecker .`
- [ ] Validate Markdown: `markdownlint *.md`

---

## 🆘 Help & Support

**Can't find what you're looking for?**

| Question | File | Section |
|----------|------|---------|
| How do I get started? | [QUICKSTART.md](QUICKSTART.md) | Installation |
| How does the system work? | [OVERVIEW.md](OVERVIEW.md) | System Architecture |
| How do I run tests? | [TESTING.md](TESTING.md) | Quick Start |
| How do CI/CD workflows work? | [WORKFLOWS.md](WORKFLOWS.md) | Workflow Overview |
| What's wrong with my tests? | [CI-CD-QUICK-REF.md](CI-CD-QUICK-REF.md) | Troubleshooting |
| How do I connect sensors? | [example_integration.py](example_integration.py) | Integration Examples |
| How is code structured? | [IMPLEMENTATION.md](IMPLEMENTATION.md) | Project Structure |

---

**Last Updated:** 2024
**Total Documentation:** 12+ comprehensive guides
**Test Coverage:** 51+ automated tests
**Workflows:** 7 GitHub Actions workflows
