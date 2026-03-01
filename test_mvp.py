#!/usr/bin/env python3
"""
test_mvp.py
-----------
Simple script to test TreeTalk AI MVP endpoints.

Usage:
  python test_mvp.py
"""

import sys
import json
import httpx
from typing import Dict, Optional

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 30.0

# Color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{CYAN}{BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}❌ {text}{RESET}")


def print_info(text: str):
    """Print info message."""
    print(f"{CYAN}ℹ️  {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠️  {text}{RESET}")


def test_health_check() -> bool:
    """Test GET / endpoint."""
    print_header("Test 1: Health Check")
    
    try:
        response = httpx.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            print_success("Health check passed")
            data = response.json()
            print(f"  Status: {data.get('status')}")
            print(f"  Version: {data.get('version')}")
            print(f"  Available endpoints:")
            for endpoint, desc in data.get('endpoints', {}).items():
                print(f"    - {endpoint}: {desc}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Could not connect to API: {e}")
        print_warning("Make sure the API server is running:")
        print_warning("  python -m uvicorn api.main:app --reload")
        return False


def test_scenarios() -> bool:
    """Test GET /scenarios endpoint."""
    print_header("Test 2: Get Available Scenarios")
    
    try:
        response = httpx.get(f"{BASE_URL}/scenarios", timeout=TIMEOUT)
        if response.status_code == 200:
            print_success("Scenarios retrieved")
            data = response.json()
            print(f"  Available scenarios:")
            for scenario in data.get('scenarios', []):
                print(f"    - {scenario}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


def test_mock_analyze(scenario: str, tree_name: str = "Test Tree") -> bool:
    """Test GET /mock-analyze/{scenario} endpoint."""
    print_header(f"Test 3: Mock Analysis - {scenario.upper()}")
    
    try:
        url = f"{BASE_URL}/mock-analyze/{scenario}"
        print_info(f"Requesting: {url}")
        
        response = httpx.get(url, params={"tree_name": tree_name}, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_success(f"Analysis completed for: {tree_name}")
            data = response.json()
            
            print(f"\n  Tree: {data.get('tree_name')}")
            print(f"  Timestamp: {data.get('timestamp')}")
            print(f"  Severity: {data.get('severity')}")
            print(f"\n  {BOLD}Health Report:{RESET}")
            print(f"  {'-'*56}")
            
            # Print first 500 characters of analysis
            analysis = data.get('analysis', '')
            if len(analysis) > 500:
                print(f"  {analysis[:500]}...")
                print(f"\n  [Full report truncated. Length: {len(analysis)} chars]")
            else:
                print(f"  {analysis}")
            
            return True
        else:
            print_error(f"Analysis failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except httpx.TimeoutException:
        print_warning(f"Request timed out after {TIMEOUT}s")
        print_info("Gemini API might be slow. Try again or check your internet connection.")
        return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


def test_real_analyze() -> bool:
    """Test POST /analyze endpoint with sample data."""
    print_header("Test 4: Real Analysis (Sample Data)")
    
    # Healthy sensor data
    sensor_data = {
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
        "tree_name": "Sample Tree"
    }
    
    try:
        print_info("Sending sample sensor data...")
        response = httpx.post(
            f"{BASE_URL}/analyze",
            json=sensor_data,
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            print_success("Real analysis completed")
            data = response.json()
            
            print(f"\n  Tree: {data.get('tree_name')}")
            print(f"  Timestamp: {data.get('timestamp')}")
            print(f"  Severity: {data.get('severity')}")
            print(f"\n  {BOLD}Health Report:{RESET}")
            print(f"  {'-'*56}")
            
            # Print first 500 characters of analysis
            analysis = data.get('analysis', '')
            if len(analysis) > 500:
                print(f"  {analysis[:500]}...")
                print(f"\n  [Full report truncated. Length: {len(analysis)} chars]")
            else:
                print(f"  {analysis}")
            
            return True
        else:
            print_error(f"Analysis failed with status {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
            
    except httpx.TimeoutException:
        print_warning(f"Request timed out after {TIMEOUT}s")
        print_info("Gemini API might be slow. Try again or check your internet connection.")
        return False
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False


def run_all_tests():
    """Run all MVP tests."""
    print(f"\n{BOLD}{CYAN}🌳 TreeTalk AI - MVP Test Suite{RESET}\n")
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    if not results[0][1]:
        print_error("Cannot proceed - API server not responding")
        return False
    
    # Test 2: Scenarios
    results.append(("Get Scenarios", test_scenarios()))
    
    # Test 3: Mock analysis (healthy scenario)
    results.append(("Mock Analysis (Healthy)", test_mock_analyze("healthy", "Oak Tree")))
    
    # Test 4: Real analysis
    results.append(("Real Analysis", test_real_analyze()))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {status}: {test_name}")
    
    print(f"\n  {BOLD}Total: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print_success("\n✨ All MVP tests passed! The system is working correctly.\n")
        return True
    else:
        print_error(f"\n⚠️  {total - passed} test(s) failed. See details above.\n")
        return False


def main():
    """Main entry point."""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
