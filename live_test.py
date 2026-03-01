#!/usr/bin/env python3
"""
live_test.py
-----------
Live integration tests for TreeTalk AI API.

Tests the actual running API endpoints with real HTTP requests.

Requirements:
  - API must be running: python -m uvicorn api.main:app --reload
  - httpx installed (in requirements.txt)

Run with: python live_test.py

Exit codes:
  0 = All live tests passed ✅
  1 = Live tests failed ❌
"""

import sys
import json
import time
from typing import Optional, Dict, Any
from datetime import datetime

try:
    import httpx
except ImportError:
    print("❌ httpx is required. Install with: pip install httpx")
    sys.exit(1)

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header(text: str):
    """Print formatted test header."""
    print(f"\n{CYAN}{BOLD}{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}{RESET}\n")


def print_pass(test_name: str, details: str = ""):
    """Print passing test."""
    print(f"{GREEN}✅ PASS{RESET}: {test_name}")
    if details:
        print(f"       {details}")


def print_fail(test_name: str, reason: str = ""):
    """Print failing test."""
    print(f"{RED}❌ FAIL{RESET}: {test_name}")
    if reason:
        print(f"       {RED}→ {reason}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{CYAN}ℹ️ {text}{RESET}")


class LiveTestSuite:
    """Live tests against running API."""
    
    def __init__(self, api_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.api_url = api_url
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
        self.passed = 0
        self.failed = 0
    
    def run_all(self) -> bool:
        """Run all live tests."""
        print_header("TreeTalk AI - Live API Test Suite")
        
        # Check if API is reachable
        if not self.check_api_health():
            print_fail("API Health", f"Cannot connect to {self.api_url}")
            print(f"\n{YELLOW}Make sure API is running:{RESET}")
            print(f"  python -m uvicorn api.main:app --reload\n")
            return False
        
        # Run all test groups
        self.test_endpoints()
        self.test_health_check()
        self.test_scenarios_endpoint()
        self.test_mock_analysis()
        self.test_real_analysis()
        self.test_error_handling()
        self.test_response_validation()
        
        # Print summary
        self.print_summary()
        
        return self.failed == 0
    
    def check_api_health(self) -> bool:
        """Quick check if API is responding."""
        try:
            response = self.client.get(f"{self.api_url}/", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False
    
    def test_endpoints(self):
        """Test 1: Verify all endpoints exist."""
        print_header("Test 1: API Endpoints")
        
        endpoints = [
            ("GET", "/", "Health check"),
            ("GET", "/scenarios", "List scenarios"),
            ("GET", "/mock-analyze/healthy", "Mock analysis"),
            ("POST", "/analyze", "Real analysis"),
        ]
        
        for method, path, description in endpoints:
            try:
                if method == "GET":
                    response = self.client.get(f"{self.api_url}{path}")
                else:
                    # POST with minimal valid data
                    response = self.client.post(
                        f"{self.api_url}{path}",
                        json=self._get_valid_sensor_data()
                    )
                
                if response.status_code in [200, 400, 422]:  # Expected codes
                    print_pass(f"{method} {path}", f"{description} - HTTP {response.status_code}")
                    self.passed += 1
                else:
                    print_fail(
                        f"{method} {path}",
                        f"Unexpected status {response.status_code}"
                    )
                    self.failed += 1
            except Exception as e:
                print_fail(f"{method} {path}", str(e))
                self.failed += 1
    
    def test_health_check(self):
        """Test 2: Health check endpoint."""
        print_header("Test 2: Health Check Endpoint")
        
        try:
            response = self.client.get(f"{self.api_url}/")
            assert response.status_code == 200, f"HTTP {response.status_code}"
            
            data = response.json()
            assert 'status' in data, "Missing 'status' field"
            assert 'version' in data, "Missing 'version' field"
            assert 'endpoints' in data, "Missing 'endpoints' field"
            
            print_pass("GET /", f"Status: {data.get('status')}")
            print_info(f"Version: {data.get('version')}")
            self.passed += 1
            
        except Exception as e:
            print_fail("GET /", str(e))
            self.failed += 1
    
    def test_scenarios_endpoint(self):
        """Test 3: Scenarios endpoint."""
        print_header("Test 3: Scenarios Endpoint")
        
        try:
            response = self.client.get(f"{self.api_url}/scenarios")
            assert response.status_code == 200, f"HTTP {response.status_code}"
            
            data = response.json()
            assert 'scenarios' in data, "Missing 'scenarios' field"
            assert isinstance(data['scenarios'], list), "'scenarios' must be a list"
            
            expected_scenarios = [
                'healthy', 'drought_stress', 'overwatering',
                'pest_infestation', 'nutrient_deficiency'
            ]
            
            for scenario in expected_scenarios:
                assert scenario in data['scenarios'], f"Missing scenario: {scenario}"
            
            print_pass("GET /scenarios", f"Found {len(data['scenarios'])} scenarios")
            for scenario in data['scenarios']:
                print_info(f"  ✓ {scenario}")
            
            self.passed += 1
            
        except Exception as e:
            print_fail("GET /scenarios", str(e))
            self.failed += 1
    
    def test_mock_analysis(self):
        """Test 4: Mock analysis endpoint."""
        print_header("Test 4: Mock Analysis Endpoint")
        
        scenarios = ['healthy', 'drought_stress', 'overwatering']
        
        for scenario in scenarios:
            try:
                response = self.client.get(
                    f"{self.api_url}/mock-analyze/{scenario}",
                    params={"tree_name": f"Test {scenario.title()}"}
                )
                
                assert response.status_code == 200, f"HTTP {response.status_code}"
                
                data = response.json()
                assert 'tree_name' in data, "Missing 'tree_name'"
                assert 'timestamp' in data, "Missing 'timestamp'"
                assert 'health_status' in data, "Missing 'health_status'"
                assert 'analysis' in data, "Missing 'analysis'"
                assert 'severity' in data, "Missing 'severity'"
                
                assert data['severity'] in ['CRITICAL', 'WARNING', 'CAUTION', 'HEALTHY'], \
                    f"Invalid severity: {data['severity']}"
                
                analysis_len = len(data.get('analysis', ''))
                print_pass(
                    f"GET /mock-analyze/{scenario}",
                    f"Analysis: {analysis_len} chars, Severity: {data['severity']}"
                )
                self.passed += 1
                
            except Exception as e:
                print_fail(f"GET /mock-analyze/{scenario}", str(e))
                self.failed += 1
    
    def test_real_analysis(self):
        """Test 5: Real analysis endpoint."""
        print_header("Test 5: Real Analysis Endpoint")
        
        try:
            sensor_data = self._get_valid_sensor_data()
            sensor_data['tree_name'] = 'Live Test Tree'
            sensor_data['timestamp'] = datetime.now().isoformat()
            
            response = self.client.post(
                f"{self.api_url}/analyze",
                json=sensor_data,
                timeout=self.timeout
            )
            
            assert response.status_code == 200, f"HTTP {response.status_code}"
            
            data = response.json()
            assert 'tree_name' in data, "Missing 'tree_name'"
            assert data['tree_name'] == 'Live Test Tree', "Tree name mismatch"
            assert 'analysis' in data, "Missing 'analysis'"
            assert 'severity' in data, "Missing 'severity'"
            
            analysis_len = len(data.get('analysis', ''))
            print_pass(
                "POST /analyze (Real Sensor Data)",
                f"Analysis: {analysis_len} chars, Severity: {data['severity']}"
            )
            self.passed += 1
            
        except httpx.TimeoutException:
            print_fail("POST /analyze", "Request timeout - Gemini API may be slow")
            self.failed += 1
        except Exception as e:
            print_fail("POST /analyze", str(e))
            self.failed += 1
    
    def test_error_handling(self):
        """Test 6: Error handling."""
        print_header("Test 6: Error Handling")
        
        # Test 6a: Invalid scenario
        try:
            response = self.client.get(f"{self.api_url}/mock-analyze/invalid_scenario")
            assert response.status_code == 400, f"Expected 400, got {response.status_code}"
            print_pass("Invalid scenario rejection", "HTTP 400 returned correctly")
            self.passed += 1
        except Exception as e:
            print_fail("Invalid scenario rejection", str(e))
            self.failed += 1
        
        # Test 6b: Missing required field
        try:
            invalid_data = {
                'soil_moisture_pct': 55.0,
                # Missing other required fields
            }
            response = self.client.post(
                f"{self.api_url}/analyze",
                json=invalid_data
            )
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"
            print_pass("Missing field validation", "HTTP 422 returned correctly")
            self.passed += 1
        except Exception as e:
            print_fail("Missing field validation", str(e))
            self.failed += 1
    
    def test_response_validation(self):
        """Test 7: Response validation."""
        print_header("Test 7: Response Validation")
        
        try:
            response = self.client.get(
                f"{self.api_url}/mock-analyze/healthy",
                params={"tree_name": "Validation Test"}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Test 7a: Required fields
            required_fields = ['tree_name', 'timestamp', 'health_status', 'analysis', 'severity']
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"
            
            print_pass("Response structure", "All required fields present")
            self.passed += 1
            
            # Test 7b: Field types and content
            assert isinstance(data['tree_name'], str), "tree_name must be string"
            assert isinstance(data['timestamp'], str), "timestamp must be string"
            assert isinstance(data['analysis'], str), "analysis must be string"
            assert len(data['analysis']) > 100, "analysis too short"
            
            print_pass("Field types and content", "All fields have correct types")
            self.passed += 1
            
            # Test 7c: JSON structure validity
            json_str = json.dumps(data)
            parsed = json.loads(json_str)
            assert parsed == data, "JSON serialization failed"
            
            print_pass("JSON validity", "Response is valid JSON")
            self.passed += 1
            
        except Exception as e:
            print_fail("Response validation", str(e))
            self.failed += 1
    
    def print_summary(self):
        """Print test summary."""
        print_header("Live Test Summary")
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"{BOLD}Results:{RESET}")
        print(f"  {GREEN}Passed: {self.passed}{RESET}")
        print(f"  {RED}Failed: {self.failed}{RESET}")
        print(f"  {CYAN}Total:  {total}{RESET}")
        print(f"  {BOLD}Pass Rate: {pass_rate:.1f}%{RESET}\n")
        
        if self.failed == 0:
            print(f"{GREEN}{BOLD}✅ ALL LIVE TESTS PASSED!{RESET}")
            print(f"   API is working correctly and ready for production! 🚀\n")
        else:
            print(f"{RED}{BOLD}❌ SOME TESTS FAILED!{RESET}")
            print(f"   Check the API logs and fix the issues above.\n")
    
    @staticmethod
    def _get_valid_sensor_data() -> Dict[str, Any]:
        """Get valid sensor data for testing."""
        return {
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


def main():
    """Run live test suite."""
    print_header("TreeTalk AI - Live Integration Tests")
    print_info("Make sure the API is running:")
    print_info("  python -m uvicorn api.main:app --reload")
    print("")
    
    time.sleep(1)  # Give user time to read the message
    
    try:
        suite = LiveTestSuite()
        success = suite.run_all()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Live tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
