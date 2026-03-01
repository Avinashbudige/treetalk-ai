#!/usr/bin/env python3
"""
example_integration.py
---------------------
Example showing how to integrate real IoT sensor data into TreeTalk AI.

This demonstrates:
1. Reading sensor data from various sources
2. Formatting it for the API
3. Sending it to the REST endpoint
4. Processing the response

Use this as a template for your actual IoT integration.
"""

import json
import httpx
from datetime import datetime
from typing import Dict, Optional

# API configuration
API_BASE_URL = "http://localhost:8000"
SENSOR_TIMEOUT = 30.0


class TreeHealthMonitor:
    """
    Example class for integrating real sensor data with TreeTalk AI.
    """
    
    def __init__(self, api_url: str = API_BASE_URL, tree_name: str = "Unknown Tree"):
        """
        Initialize the monitor.
        
        Args:
            api_url: Base URL of the TreeTalk API
            tree_name: Name identifier for the tree
        """
        self.api_url = api_url
        self.tree_name = tree_name
        self.client = httpx.Client(timeout=SENSOR_TIMEOUT)
    
    def read_sensors_from_gpio(self) -> Dict:
        """
        Example: Read sensors connected to Raspberry Pi GPIO pins.
        
        This is a TEMPLATE - replace with your actual GPIO reading code.
        Common libraries:
        - RPi.GPIO for GPIO pins
        - Adafruit libraries for specific sensors
        - PySerial for serial sensors
        
        Returns:
            Dictionary with 14 sensor values
        """
        # Example: Using Adafruit libraries (you would install these)
        # from Adafruit_ADS1x15 import ADS1115
        # from board import SCL, SDA
        # import busio
        # import adafruit_bmp280
        
        # This is placeholder code - REPLACE WITH YOUR HARDWARE
        sensor_data = {
            "soil_moisture_pct": self._read_soil_moisture(),        # Example: 0-100% analog sensor
            "soil_temperature_c": self._read_soil_temp(),           # Example: DS18B20 temp sensor
            "soil_ph": self._read_soil_ph(),                        # Example: Analog pH probe
            "soil_ec_mS_cm": self._read_soil_ec(),                  # Example: Conductivity sensor
            "air_temperature_c": self._read_air_temp(),             # Example: DHT22
            "air_humidity_pct": self._read_air_humidity(),          # Example: DHT22
            "light_lux": self._read_light(),                        # Example: BH1750 lux sensor
            "co2_ppm": self._read_co2(),                            # Example: MH-Z19B CO2 sensor
            "trunk_diameter_mm": self._read_trunk_diameter(),       # Example: Ultrasonic or laser
            "sap_flow_L_hr": self._read_sap_flow(),                 # Example: Granier sap flow sensor
            "leaf_temperature_c": self._read_leaf_temp(),           # Example: IR thermometer
            "vibration_amplitude_g": self._read_vibration(),        # Example: ADXL345 accelerometer
            "rainfall_mm_24h": self._read_rainfall(),               # Example: Tipping bucket rain gauge
            "wind_speed_km_h": self._read_wind_speed(),             # Example: Anemometer
        }
        
        return sensor_data
    
    def read_sensors_from_csv(self, csv_file: str) -> Dict:
        """
        Example: Read the latest sensor reading from a CSV file.
        
        CSV Format:
        timestamp,soil_moisture_pct,soil_temperature_c,soil_ph,...
        2026-03-01T10:00:00Z,55.2,20.1,6.5,...
        
        Args:
            csv_file: Path to CSV file with sensor data
            
        Returns:
            Dictionary with latest sensor reading
        """
        import csv
        
        sensor_data = {}
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                # Get the last row
                last_row = rows[-1]
                # Convert string values to floats
                for key, value in last_row.items():
                    if key != 'timestamp':
                        try:
                            sensor_data[key] = float(value)
                        except ValueError:
                            sensor_data[key] = 0.0
        
        return sensor_data
    
    def read_sensors_from_api(self, sensor_api_url: str) -> Dict:
        """
        Example: Read sensor data from another API (e.g., IoT platform).
        
        Many IoT platforms provide REST APIs (Ubidots, Thingspeak, etc.)
        
        Args:
            sensor_api_url: URL of the sensor data API
            
        Returns:
            Dictionary with sensor values
        """
        try:
            response = httpx.get(sensor_api_url, timeout=SENSOR_TIMEOUT)
            data = response.json()
            
            # Map the response fields to TreeTalk schema
            sensor_data = {
                "soil_moisture_pct": data.get("moisture", 0),
                "soil_temperature_c": data.get("temp_soil", 0),
                "soil_ph": data.get("ph", 6.5),
                # ... map other fields ...
            }
            
            return sensor_data
        except Exception as e:
            print(f"Error reading from sensor API: {e}")
            return {}
    
    def read_sensors_from_simulator(self) -> Dict:
        """
        Example: Generate simulated sensor data (for testing).
        
        This is useful for testing without physical sensors.
        """
        import random
        
        # Generate realistic but fake sensor data
        sensor_data = {
            "soil_moisture_pct": random.uniform(40, 70),
            "soil_temperature_c": random.uniform(15, 25),
            "soil_ph": random.uniform(6.0, 7.0),
            "soil_ec_mS_cm": random.uniform(1.0, 2.0),
            "air_temperature_c": random.uniform(15, 30),
            "air_humidity_pct": random.uniform(40, 80),
            "light_lux": random.uniform(20000, 50000),
            "co2_ppm": random.uniform(380, 420),
            "trunk_diameter_mm": 150 + random.uniform(-2, 2),
            "sap_flow_L_hr": random.uniform(1.5, 3.0),
            "leaf_temperature_c": random.uniform(20, 30),
            "vibration_amplitude_g": random.uniform(0.01, 0.05),
            "rainfall_mm_24h": random.uniform(0, 10),
            "wind_speed_km_h": random.uniform(5, 20),
        }
        
        return sensor_data
    
    # ========================================================================
    # INDIVIDUAL SENSOR READING EXAMPLES (Replace with your code)
    # ========================================================================
    
    def _read_soil_moisture(self) -> float:
        """Read soil moisture sensor (0-100%)."""
        # Example: ADC0 pin on ADS1115
        # value = ads.read_adc(0, gain=1)  # Raw: 0-32767
        # percentage = (value / 32767) * 100
        # return round(percentage, 1)
        return 55.0  # Placeholder
    
    def _read_soil_temp(self) -> float:
        """Read soil temperature sensor (DS18B20)."""
        # Example: W1 temperature sensor
        # import glob
        # base_dir = '/sys/bus/w1/devices/'
        # device_folder = glob.glob(base_dir + '28*')[0]
        # device_file = device_folder + '/w1_slave'
        # with open(device_file) as f:
        #     lines = f.readlines()
        # temp_pos = lines[1].find('t=')
        # temp_c = float(lines[1][temp_pos+2:]) / 1000
        # return round(temp_c, 1)
        return 20.0  # Placeholder
    
    def _read_soil_ph(self) -> float:
        """Read pH sensor."""
        # Example: Analog pH probe + ADC
        # voltage = read_adc(pin=1)
        # ph = 3.5 * voltage / 4095 + 0   # Calibrate for your sensor
        # return round(ph, 2)
        return 6.5  # Placeholder
    
    def _read_soil_ec(self) -> float:
        """Read electrical conductivity (soil nutrients)."""
        # Example: EC sensor
        # voltage = read_adc(pin=2)
        # ec = (voltage / 4095) * 5   # mS/cm
        # return round(ec, 2)
        return 1.5  # Placeholder
    
    def _read_air_temp(self) -> float:
        """Read air temperature (DHT22)."""
        # Example: DHT22 sensor
        # import Adafruit_DHT
        # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        # return round(temperature, 1)
        return 25.0  # Placeholder
    
    def _read_air_humidity(self) -> float:
        """Read air humidity (DHT22)."""
        # Example: DHT22 sensor
        # import Adafruit_DHT
        # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        # return round(humidity, 1)
        return 60.0  # Placeholder
    
    def _read_light(self) -> float:
        """Read light intensity (LUX) - BH1750 sensor."""
        # Example: BH1750 I2C light sensor
        # import smbus2
        # bus = smbus2.SMBus(1)
        # data = bus.read_i2c_block_data(0x23, 0x10, 2)
        # lux = (data[0] << 8 | data[1]) / 1.2
        # return int(lux)
        return 40000  # Placeholder
    
    def _read_co2(self) -> float:
        """Read CO2 level - MH-Z19B sensor."""
        # Example: MH-Z19B CO2 sensor on serial
        # import serial
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        # command = bytes([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
        # ser.write(command)
        # response = ser.read(9)
        # ppm = (response[2] * 256) + response[3]
        # return ppm
        return 420  # Placeholder
    
    def _read_trunk_diameter(self) -> float:
        """Read trunk diameter using ultrasonic or laser sensor."""
        # Example: HC-SR04 ultrasonic sensor
        # distance = measure_distance_cm()
        # diameter = distance * 2  # Simple approximation
        # return round(diameter, 1)
        return 152.0  # Placeholder
    
    def _read_sap_flow(self) -> float:
        """Read sap flow using Granier sensor."""
        # Example: Granier sap flow sensor (specialized)
        # This typically requires specialized equipment and calibration
        # Usually connected via analog ADC
        # voltage = read_adc(pin=5)
        # flow = (voltage / 4095) * 5   # L/hr (calibration needed)
        # return round(flow, 2)
        return 2.0  # Placeholder
    
    def _read_leaf_temp(self) -> float:
        """Read leaf temperature using IR thermometer."""
        # Example: MLX90614 IR sensor
        # from adafruit_circuitpython_mlx90614 import Adafruit_MLX90614
        # sensor = Adafruit_MLX90614()
        # return round(sensor.object_temperature, 1)
        return 26.0  # Placeholder
    
    def _read_vibration(self) -> float:
        """Read trunk vibration using accelerometer."""
        # Example: ADXL345 accelerometer
        # from adafruit_adxl34x import ADXL345
        # sensor = ADXL345()
        # x, y, z = sensor.acceleration
        # g_force = (x**2 + y**2 + z**2)**0.5 / 9.81
        # return round(g_force, 3)
        return 0.05  # Placeholder
    
    def _read_rainfall(self) -> float:
        """Read rainfall (24h tipping bucket gauge)."""
        # Example: Tipping bucket rain gauge
        # Each tip = 0.01 inch = 0.254 mm
        # Read GPIO pin count for today
        # tips_today = count_gpio_pulses()
        # mm_24h = tips_today * 0.254
        # return round(mm_24h, 1)
        return 2.0  # Placeholder
    
    def _read_wind_speed(self) -> float:
        """Read wind speed from anemometer."""
        # Example: 3-cup anemometer
        # Typically 2.4 km/h per cup rotation
        # pulses_per_second = count_gpio_pulses()
        # speed = pulses_per_second * 2.4
        # return round(speed, 1)
        return 12.0  # Placeholder
    
    # ========================================================================
    # ANALYSIS & REPORTING
    # ========================================================================
    
    def analyze_tree(self, sensor_data: Optional[Dict] = None) -> Dict:
        """
        Analyze the tree using TreeTalk AI.
        
        Args:
            sensor_data: Optional sensor readings. If not provided, reads sensors.
            
        Returns:
            Health report from the API
        """
        # Read sensors if not provided
        if sensor_data is None:
            print(f"📡 Reading sensors for {self.tree_name}...")
            # Choose your data source:
            # sensor_data = self.read_sensors_from_gpio()
            # sensor_data = self.read_sensors_from_csv("data.csv")
            # sensor_data = self.read_sensors_from_api("http://...")
            sensor_data = self.read_sensors_from_simulator()  # For testing
        
        # Add metadata
        sensor_data["tree_name"] = self.tree_name
        sensor_data["timestamp"] = datetime.now().isoformat()
        
        print(f"🔍 Analyzing tree health...")
        
        # Send to TreeTalk API
        try:
            response = self.client.post(
                f"{self.api_url}/analyze",
                json=sensor_data,
                timeout=SENSOR_TIMEOUT
            )
            
            if response.status_code == 200:
                report = response.json()
                return report
            else:
                print(f"❌ API error: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return {}
        
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return {}
    
    def print_report(self, report: Dict):
        """
        Pretty-print the health report.
        
        Args:
            report: Health report from analyze_tree()
        """
        if not report:
            print("❌ No report available")
            return
        
        print("\n" + "="*60)
        print(f"🌳 TREE HEALTH REPORT: {report.get('tree_name', 'Unknown')}")
        print("="*60)
        
        print(f"\n📅 Timestamp: {report.get('timestamp')}")
        print(f"🚨 Severity: {report.get('severity')}")
        print(f"📊 Status: {report.get('health_status')}")
        
        print("\n" + "-"*60)
        print("📋 ANALYSIS:")
        print("-"*60)
        print(report.get('analysis', 'No analysis available'))
        print("\n" + "="*60)
    
    def log_report(self, report: Dict, log_file: str = "tree_health_log.jsonl"):
        """
        Append health report to log file (JSONL format).
        
        Args:
            report: Health report from analyze_tree()
            log_file: Path to log file
        """
        if not report:
            return
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(report) + '\n')
        
        print(f"✅ Report logged to {log_file}")


def main():
    """Example: Monitor a tree in real-time."""
    
    # Create monitor
    monitor = TreeHealthMonitor(tree_name="Garden Oak #1")
    
    # Analyze tree
    report = monitor.analyze_tree()
    
    # Display and log the report
    monitor.print_report(report)
    monitor.log_report(report)
    
    # Check if tree needs attention
    severity = report.get('severity', 'UNKNOWN')
    if severity in ['CRITICAL', 'WARNING']:
        print(f"\n⚠️  ALERT: Tree requires attention! Severity: {severity}")
        # Here you could send SMS, email, or webhook notifications


if __name__ == "__main__":
    main()
