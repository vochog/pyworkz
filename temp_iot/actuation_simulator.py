"""
Actuation Simulator Script

This script simulates changing the thermostat setpoint based on decisions from
the Decision Engine. It reads the decisions log and simulates the appropriate
action, logging the simulated actions to a separate file.

Note: This is just a simulation - no actual hardware is controlled.
"""

import os
import time
from datetime import datetime

# Configuration
LOG_DIR = 'logs'
DECISION_LOG = os.path.join(LOG_DIR, 'decisions.log')
ACTION_LOG = os.path.join(LOG_DIR, 'actions.log')
INTERVAL = 60  # seconds

def get_latest_decision():
    """Read the latest decision from the decision log file."""
    if not os.path.exists(DECISION_LOG):
        return None
    
    with open(DECISION_LOG, 'r') as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        return last_line.split(',')

def simulate_action(decision):
    """Simulate the appropriate action based on the decision."""
    action = None
    
    if "raise setpoint" in decision.lower():
        action = "SIMULATED ACTION: Thermostat setpoint increased by 1°C"
    elif "lower setpoint" in decision.lower():
        action = "SIMULATED ACTION: Thermostat setpoint decreased by 1°C"
    else:
        action = "SIMULATED ACTION: No change to thermostat"
    
    return action

def log_action(action):
    """Log the simulated action with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp},{action}\n"
    
    with open(ACTION_LOG, 'a') as file:
        file.write(log_entry)
    
    print(f"Action logged at {timestamp}: {action}")

def main():
    print("Actuation Simulator started. Press Ctrl+C to stop.")
    try:
        while True:
            # Get the latest decision
            decision_data = get_latest_decision()
            
            if decision_data:
                timestamp, decision = decision_data
                action = simulate_action(decision)
                log_action(action)
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nActuation Simulator stopped.")

if __name__ == "__main__":
    main()