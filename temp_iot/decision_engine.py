"""
Decision Engine Script

This script analyzes sensor data from the log file and makes decisions about
whether to raise or lower the room temperature based on comfort rules.

Comfort Rules:
- Occupied rooms must stay within 20–24°C
- If unoccupied and too hot, log "lower setpoint"
- If occupied and too cold, log "raise setpoint"
- If within range, do nothing
- Always log decisions with timestamps
"""

import os
import time
from datetime import datetime

# Configuration
LOG_DIR = 'logs'
SENSOR_LOG = os.path.join(LOG_DIR, 'sensor_data.log')
DECISION_LOG = os.path.join(LOG_DIR, 'decisions.log')
INTERVAL = 60  # seconds

def get_latest_sensor_data():
    """Read the latest entry from the sensor log file."""
    if not os.path.exists(SENSOR_LOG):
        return None
    
    with open(SENSOR_LOG, 'r') as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        return last_line.split(',')

def make_decision(temperature, occupancy):
    """Make a decision based on temperature and occupancy status."""
    temp = float(temperature)
    occupied = occupancy == '1'
    
    if occupied:
        if temp < 20:
            return "raise setpoint"
        elif temp > 24:
            return "lower setpoint"
        else:
            return "within comfort range"
    else:  # unoccupied
        if temp > 24:
            return "lower setpoint (unoccupied)"
        else:
            return "no action needed (unoccupied)"

def log_decision(decision):
    """Log the decision with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{decision}\n"
    
    with open(DECISION_LOG, 'a') as file:
        file.write(log_entry)
    
    print(f"Decision logged at {timestamp}: {decision}")

def main():
    print("Decision Engine started. Press Ctrl+C to stop.")
    try:
        while True:
            # Get the latest sensor data
            sensor_data = get_latest_sensor_data()
            
            if sensor_data:
                timestamp, temperature, power, occupancy = sensor_data
                decision = make_decision(temperature, occupancy)
                log_decision(decision)
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nDecision Engine stopped.")

if __name__ == "__main__":
    main()