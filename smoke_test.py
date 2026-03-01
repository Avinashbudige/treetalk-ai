#!/usr/bin/env python3
"""
smoke_test.py
-------------
Smoke tests for TreeTalk AI MVP.

A smoke test is a quick sanity check that verifies the core functionality
of the application without requiring external services (like Gemini API).

Run with: python smoke_test.py

Exit codes:
  0 = All smoke tests passed ✅
  1 = Smoke tests failed ❌
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str):
    """Print formatted test header."""
    print(f"\n{CYAN}{BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")


def print_pass(test_name: str):
    """Print passing test."""
    print(f"{GREEN}✅ PASS{RESET}: {test_name}")


def print_fail(test_name: str, reason: str = ""):
    """Print failing test."""
    print(f"{RED}❌ FAIL{RESET}: {test_name}")
    if reason:
        print(f"       {RED}→ {reason}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{CYAN}ℹ️ {text}{RESET}")


class SmokeTestSuite:
    """Smoke test suite for TreeTalk AI."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def run_all(self) -> bool:
        """Run all smoke tests."""
        print_header("TreeTalk AI - Smoke Test Suite")
        
        # Test groups
        self.test_imports()
        self.test_file_structure()
        self.test_prompt_system()
        self.test_sensor_data()
        self.test_api_models()
        self.test_integration()
        
        # Print summary
        self.print_summary()
        
        return self.failed == 0
    
    def test_imports(self):
        """Test 1: Verify all critical imports work."""
        print_header("Test 1: Critical Imports")
        
        try:
            from ai.gemini_health_prompt import (
                get_system_prompt,
                get_analysis_prompt,
                get_quick_reference_guide
            )
            print_pass("Import ai.gemini_health_prompt")
            self.passed += 1
        except ImportError as e:
            print_fail("Import ai.gemini_health_prompt", str(e))
            self.failed += 1
        
        try:
            from api.main import (
                app,
                SensorData,
                HealthReport,
                analyze_sensor_data,
                mock_analyze,
                get_scenarios
            )
            print_pass("Import api.main")
            self.passed += 1
        except ImportError as e:
            print_fail("Import api.main", str(e))
            self.failed += 1
        
        try:
            from sensors.mock_sensor_readings import (
                SCENARIOS,
                generate_sensor_data,
                generate_reading
            )
            print_pass("Import sensors.mock_sensor_readings")
            self.passed += 1
        except ImportError as e:
            print_fail("Import sensors.mock_sensor_readings", str(e))
            self.failed += 1
        
        try:
            from example_integration import TreeHealthMonitor
            print_pass("Import example_integration")
            self.passed += 1
        except ImportError as e:
            print_fail("Import example_integration", str(e))
            self.failed += 1
    
    def test_file_structure(self):
        """Test 2: Verify project file structure."""
        print_header("Test 2: File Structure")
        
        required_files = [
            "ai/__init__.py",
            "ai/gemini_health_prompt.py",
            "api/__init__.py",
            "api/main.py",
            "sensors/__init__.py",
            "sensors/mock_sensor_readings.py",
            "example_integration.py",
            "test_mvp.py",
            "requirements.txt",
            ".env.example",
        ]
        
        for file_path in required_files:
            if Path(file_path).exists():
                print_pass(f"File exists: {file_path}")
                self.passed += 1
            else:
                print_fail(f"File missing: {file_path}")
                self.failed += 1
    
    def test_prompt_system(self):
        """Test 3: Verify prompt system functionality."""
        print_header("Test 3: Prompt System")
        
        try:
            from ai.gemini_health_prompt import (
                get_system_prompt,
                get_analysis_prompt,
                get_quick_reference_guide,
                _get_unit
            )
            
            # Test 3a: System prompt
            system = get_system_prompt()
            assert isinstance(system, str), "System prompt must be string"
            assert len(system) > 200, "System prompt too short"
            assert "arborist" in system.lower(), "System prompt missing arborist role"
            print_pass("System prompt generation")
            self.passed += 1
            
        except Exception as e:
            print_fail("System prompt generation", str(e))
            self.failed += 1
        
        try:
            # Test 3b: Analysis prompt
            test_data = {
                'soil_moisture_pct': 55.0,
                'soil_temperature_c': 20.0,
                'soil_ph': 6.5,
                'soil_ec_mS_cm': 1.5,
                'air_temperature_c': 25.0,
                'air_humidity_pct': 60.0,
                'light_lux': 40000.0,
                'co2_ppm': 420.0,
                'trunk_diameter_mm': 152.0,
                'sap_flow_L_hr': 2.0,
                'leaf_temperature_c': 26.0,
                'vibration_amplitude_g': 0.05,
                'rainfall_mm_24h': 2.0,
                'wind_speed_km_h': 12.0,
            }
            
            analysis = get_analysis_prompt(test_data, 'Test Oak')
            assert isinstance(analysis, str), "Analysis prompt must be string"
            assert len(analysis) > 500, "Analysis prompt too short"
            assert 'Test Oak' in analysis, "Tree name not in analysis"
            print_pass("Analysis prompt generation")
            self.passed += 1
            
        except Exception as e:
            print_fail("Analysis prompt generation", str(e))
            self.failed += 1
        
        try:
            # Test 3c: Quick reference guide
            guide = get_quick_reference_guide()
            assert isinstance(guide, str), "Guide must be string"
            assert 'DROUGHT' in guide.upper(), "Quick reference incomplete"
            print_pass("Quick reference guide generation")
            self.passed += 1
            
        except Exception as e:
            print_fail("Quick reference guide generation", str(e))
            self.failed += 1
    
    def test_sensor_data(self):
        """Test 4: Verify sensor data generation."""
        print_header("Test 4: Sensor Data Generation")
        
        try:
            from sensors.mock_sensor_readings import (
                SCENARIOS,
                generate_sensor_data,
                OPTIMAL_RANGES
            )
            
            # Test 4a: Scenario availability
            assert len(SCENARIOS) == 5, f"Expected 5 scenarios, got {len(SCENARIOS)}"
            expected_scenarios = [
                'healthy', 'drought_stress', 'overwatering',
                'pest_infestation', 'nutrient_deficiency'
            ]
            for scenario in expected_scenarios:
                assert scenario in SCENARIOS, f"Missing scenario: {scenario}"
            print_pass("All 5 scenarios available")
            self.passed += 1
            
        except Exception as e:
            print_fail("Scenario availability", str(e))
            self.failed += 1
        
        try:
            # Test 4b: Data generation for each scenario
            from sensors.mock_sensor_readings import generate_sensor_data
            
            required_fields = [
                'soil_moisture_pct', 'soil_temperature_c', 'soil_ph', 'soil_ec_mS_cm',
                'air_temperature_c', 'air_humidity_pct', 'light_lux', 'co2_ppm',
                'trunk_diameter_mm', 'sap_flow_L_hr', 'leaf_temperature_c',
                'vibration_amplitude_g', 'rainfall_mm_24h', 'wind_speed_km_h'
            ]
            
            for scenario in SCENARIOS.keys():
                data = generate_sensor_data(scenario)
                for field in required_fields:
                    assert field in data, f"Missing {field} in {scenario}"
            
            print_pass("Data generation for all scenarios")
            self.passed += 1
            
        except Exception as e:
            print_fail("Data generation for all scenarios", str(e))
            self.failed += 1
        
        try:
            # Test 4c: Healthy range definitions
            from sensors.mock_sensor_readings import OPTIMAL_RANGES
            
            assert len(OPTIMAL_RANGES) > 0, "No optimal ranges defined"
            assert 'soil_moisture_pct' in OPTIMAL_RANGES, "Missing soil moisture range"
            assert 'light_lux' in OPTIMAL_RANGES, "Missing light range"
            print_pass("Optimal ranges defined")
            self.passed += 1
            
        except Exception as e:
            print_fail("Optimal ranges defined", str(e))
            self.failed += 1
    
    def test_api_models(self):
        """Test 5: Verify API data models."""
        print_header("Test 5: API Models & Validation")
        
        try:
            from api.main import SensorData
            from pydantic import ValidationError
            
            # Test 5a: Valid data passes
            valid_data = {
                'soil_moisture_pct': 55.0,
                'soil_temperature_c': 20.0,
                'soil_ph': 6.5,
                'soil_ec_mS_cm': 1.5,
                'air_temperature_c': 25.0,
                'air_humidity_pct': 60.0,
                'light_lux': 40000.0,
                'co2_ppm': 420.0,
                'trunk_diameter_mm': 152.0,
                'sap_flow_L_hr': 2.0,
                'leaf_temperature_c': 26.0,
                'vibration_amplitude_g': 0.05,
                'rainfall_mm_24h': 2.0,
                'wind_speed_km_h': 12.0,
                'tree_name': 'Test Tree'
            }
            
            sensor = SensorData(**valid_data)
            assert sensor.tree_name == 'Test Tree'
            print_pass("SensorData validation (valid data)")
            self.passed += 1
            
        except Exception as e:
            print_fail("SensorData validation (valid data)", str(e))
            self.failed += 1
        
        try:
            # Test 5b: Invalid data fails
            from api.main import SensorData
            from pydantic import ValidationError
            
            # Missing required field
            invalid_data = {
                'soil_temperature_c': 20.0,
                # Missing soil_moisture_pct
                'air_temperature_c': 25.0,
            }
            
            try:
                sensor = SensorData(**invalid_data)
                print_fail("SensorData validation (invalid data)", "Should have failed validation")
                self.failed += 1
            except ValidationError:
                print_pass("SensorData validation (properly rejects invalid data)")
                self.passed += 1
            
        except Exception as e:
            print_fail("SensorData validation (invalid data)", str(e))
            self.failed += 1
        
        try:
            # Test 5c: HealthReport model
            from api.main import HealthReport
            
            report = HealthReport(
                tree_name='Test Tree',
                timestamp='2026-03-01T12:00:00Z',
                health_status='Analyzed',
                analysis='Test analysis',
                severity='HEALTHY'
            )
            
            assert report.severity in ['HEALTHY', 'CAUTION', 'WARNING', 'CRITICAL']
            assert report.tree_name == 'Test Tree'
            print_pass("HealthReport model validation")
            self.passed += 1
            
        except Exception as e:
            print_fail("HealthReport model validation", str(e))
            self.failed += 1
    
    def test_integration(self):
        """Test 6: Verify integration example."""
        print_header("Test 6: Integration Example")
        
        try:
            from example_integration import TreeHealthMonitor
            
            # Test 6a: Initialize monitor
            monitor = TreeHealthMonitor(tree_name='Test Tree')
            assert monitor.tree_name == 'Test Tree'
            print_pass("TreeHealthMonitor initialization")
            self.passed += 1
            
        except Exception as e:
            print_fail("TreeHealthMonitor initialization", str(e))
            self.failed += 1
        
        try:
            # Test 6b: Simulate sensor reading
            from example_integration import TreeHealthMonitor
            
            monitor = TreeHealthMonitor()
            data = monitor.read_sensors_from_simulator()
            
            required_keys = [
                'soil_moisture_pct', 'air_temperature_c', 'light_lux', 'co2_ppm'
            ]
            for key in required_keys:
                assert key in data, f"Missing {key} in simulated data"
            
            print_pass("Sensor simulation functionality")
            self.passed += 1
            
        except Exception as e:
            print_fail("Sensor simulation functionality", str(e))
            self.failed += 1
        
        try:
            # Test 6c: Report methods exist
            from example_integration import TreeHealthMonitor
            
            monitor = TreeHealthMonitor()
            assert hasattr(monitor, 'print_report')
            assert hasattr(monitor, 'log_report')
            assert callable(monitor.print_report)
            assert callable(monitor.log_report)
            
            print_pass("Report handling methods")
            self.passed += 1
            
        except Exception as e:
            print_fail("Report handling methods", str(e))
            self.failed += 1
    
    def print_summary(self):
        """Print test summary."""
        print_header("Smoke Test Summary")
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"{BOLD}Results:{RESET}")
        print(f"  {GREEN}Passed: {self.passed}{RESET}")
        print(f"  {RED}Failed: {self.failed}{RESET}")
        print(f"  {CYAN}Total:  {total}{RESET}")
        print(f"  {BOLD}Pass Rate: {pass_rate:.1f}%{RESET}\n")
        
        if self.failed == 0:
            print(f"{GREEN}{BOLD}✅ ALL SMOKE TESTS PASSED!{RESET}")
            print(f"   TreeTalk AI MVP is ${GREEN}HEALTHY{RESET} and ready to use! 🌳\n")
        else:
            print(f"{RED}{BOLD}❌ SOME TESTS FAILED!{RESET}")
            print(f"   Please fix the issues above before proceeding.\n")


def main():
    """Run smoke test suite."""
    try:
        suite = SmokeTestSuite()
        success = suite.run_all()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Smoke tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
