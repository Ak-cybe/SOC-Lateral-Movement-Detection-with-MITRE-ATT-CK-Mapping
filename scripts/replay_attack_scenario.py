import requests
import json
import time
import os
import sys
from datetime import datetime

# ================= Configuration =================
# Set these variables or export them as environment variables
SIEM_URL = os.getenv('SIEM_URL', 'http://localhost:8088/services/collector/event') # Splunk HEC example
AUTH_TOKEN = os.getenv('SIEM_TOKEN', 'YOUR_HEC_TOKEN_HERE')
INPUT_TYPE = os.getenv('SIEM_TYPE', 'splunk') # Options: 'splunk', 'elastic'
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'attack_scenario_timeline.json')
# =================================================

def send_to_splunk(event, url, token):
    headers = {'Authorization': f'Splunk {token}'}
    payload = {
        "event": event,
        "sourcetype": "WinEventLog:Security",
        "source": "simulation_script"
    }
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        print(f"[+] Sent event (Splunk): {event.get('EventID', 'Unknown')}")
    except Exception as e:
        print(f"[-] Error sending to Splunk: {e}")

def send_to_elastic(event, url, token):
    # Simplified Elastic Bulk or single doc POST (adjust index name as needed)
    headers = {'Authorization': f'ApiKey {token}', 'Content-Type': 'application/json'}
    # Assuming 'winlogbeat-*' or similar index
    elastic_url = f"{url}/winlogbeat-simulation/_doc" 
    try:
        response = requests.post(elastic_url, headers=headers, json=event, verify=False)
        response.raise_for_status()
        print(f"[+] Sent event (Elastic): {event.get('event', {}).get('code', 'Unknown')}")
    except Exception as e:
        print(f"[-] Error sending to Elastic: {e}")

def main():
    if not os.path.exists(LOG_FILE):
        print(f"Error: Log file not found at {LOG_FILE}")
        sys.exit(1)

    print(f"Reading logs from: {LOG_FILE}")
    
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON log file.")
        sys.exit(1)

    timeline = data.get('timeline', [])
    if not timeline:
        # Fallback if structure is flat or different, strictly following user prompt structure though
        print("No 'timeline' key found in JSON.")
        sys.exit(1)

    print(f"Starting replay to {INPUT_TYPE} at {SIEM_URL}...")
    
    for stage in timeline:
        stage_name = stage.get('stage', 'Unknown Stage')
        print(f"\n--- Processing Stage: {stage_name} ---")
        
        events = stage.get('events', [])
        for event in events:
            # Rebase timestamps to "Now" to ensure SIEM real-time rules trigger
            # Assuming original logs have 'TimeCreated', '@timestamp', or similar fields
            # We calculate offset from the FIRST event in the timeline to preserve relative spacing
            
            if 'TimeCreated' in event:
                # This is a simplifed rebase assuming 'TimeCreated' is ISO 8601
                # In a real scenario, you'd parse the first event time once and calculate offset
                # For this MVP, we just set it to UTC now
                event['TimeCreated'] = datetime.utcnow().isoformat() + "Z"
            
            if INPUT_TYPE == 'splunk':
                send_to_splunk(event, SIEM_URL, AUTH_TOKEN)
            elif INPUT_TYPE == 'elastic':
                # Elastic often needs '@timestamp'
                event['@timestamp'] = datetime.utcnow().isoformat() + "Z"
                send_to_elastic(event, SIEM_URL, AUTH_TOKEN)
            
            # Optional: detailed delay simulation
            time.sleep(0.1) 

    print("\nReplay completed.")

if __name__ == "__main__":
    main()
