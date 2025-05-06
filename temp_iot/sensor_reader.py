"""
Sensor Reader Script

This script reads mock sensor data from CSV files (temperature, power, occupancy) 
every minute and appends the new data to a log file.

The mock CSV files should be in a 'mock_data' directory with the following format:
- temperature.csv: timestamp,temperature
- power.csv: timestamp,power_usage
- occupancy.csv: timestamp,occupancy_status (0=unoccupied, 1=occupied)
"""

import os
import time
import csv
from datetime import datetime

# Configuration
DATA_DIR = 'mock_data'
LOG_DIR = 'logs'
SENSOR_FILES = {
    'temperature': 'temperature.csv',
    'power': 'power.csv',
    'occupancy': 'occupancy.csv'
}
LOG_FILE = os.path.join(LOG_DIR, 'sensor_data.log')
INTERVAL = 60  # seconds

def ensure_directories_exist():
    """Create required directories if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

def read_sensor_data(sensor_type):
    """Read the latest entry from a sensor CSV file."""
    filepath = os.path.join(DATA_DIR, SENSOR_FILES[sensor_type])
    
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        # Get the last line (most recent data)
        last_line = None
        for row in reader:
            if row:  # Skip empty lines
                last_line = row
        return last_line

def log_sensor_data(temperature, power, occupancy):
    """Append sensor data to the log file with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{temperature},{power},{occupancy}\n"
    
    with open(LOG_FILE, 'a') as file:
        file.write(log_entry)
    
    print(f"Logged sensor data at {timestamp}")

def main():
    ensure_directories_exist()
    
    print("Sensor Reader started. Press Ctrl+C to stop.")
    try:
        while True:
            # Read data from all sensors
            temp_data = read_sensor_data('temperature')
            power_data = read_sensor_data('power')
            occ_data = read_sensor_data('occupancy')
            
            if temp_data and power_data and occ_data:
                # Extract values (assuming format: timestamp,value)
                timestamp, temperature = temp_data
                _, power = power_data
                _, occupancy = occ_data
                
                # Log the data
                log_sensor_data(temperature, power, occupancy)
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nSensor Reader stopped.")

if __name__ == "__main__":
    main()