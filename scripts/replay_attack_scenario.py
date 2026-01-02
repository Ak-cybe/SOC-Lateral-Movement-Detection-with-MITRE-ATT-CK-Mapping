import requests
import json
import time
import os
import sys
from datetime import datetime, timedelta
from dateutil import parser as date_parser

# ================= Configuration =================
# Set these variables or export them as environment variables
SIEM_URL = os.getenv('SIEM_URL', 'http://localhost:8088/services/collector/event') # Splunk HEC example
AUTH_TOKEN = os.getenv('SIEM_TOKEN', 'YOUR_HEC_TOKEN_HERE')
INPUT_TYPE = os.getenv('SIEM_TYPE', 'splunk') # Options: 'splunk', 'elastic'
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'attack_scenario_timeline.json')
# =================================================

def send_to_splunk(event, url, token, max_retries=3):
    """Send event to Splunk HEC with retry logic."""
    headers = {'Authorization': f'Splunk {token}'}
    payload = {
        "event": event,
        "sourcetype": "WinEventLog:Security",
        "source": "simulation_script"
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, verify=False, timeout=10)
            response.raise_for_status()
            print(f"[+] Sent event (Splunk): EventID={event.get('EventID', 'Unknown')}, Time={event.get('TimeCreated', 'N/A')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"[-] Attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    return False

def send_to_elastic(event, url, token, max_retries=3):
    """Send event to Elastic with retry logic."""
    headers = {'Authorization': f'ApiKey {token}', 'Content-Type': 'application/json'}
    elastic_url = f"{url}/winlogbeat-simulation/_doc" 
    for attempt in range(max_retries):
        try:
            response = requests.post(elastic_url, headers=headers, json=event, verify=False, timeout=10)
            response.raise_for_status()
            print(f"[+] Sent event (Elastic): code={event.get('event', {}).get('code', 'Unknown')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"[-] Attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    return False

def parse_timestamp(ts_string):
    """Parse ISO 8601 timestamp string to datetime object."""
    try:
        return date_parser.isoparse(ts_string.replace('Z', '+00:00'))
    except Exception:
        return datetime.utcnow()

def rebase_timestamps(timeline):
    """
    Rebase all event timestamps relative to NOW while preserving intervals.
    This ensures correlation rules trigger correctly in real-time.
    """
    # Find the earliest timestamp across all events
    earliest_time = None
    for stage in timeline:
        for event in stage.get('events', []):
            if 'TimeCreated' in event:
                event_time = parse_timestamp(event['TimeCreated'])
                if earliest_time is None or event_time < earliest_time:
                    earliest_time = event_time
    
    if earliest_time is None:
        earliest_time = datetime.utcnow()
    
    # Calculate offset: how much to shift all timestamps
    now = datetime.utcnow()
    time_offset = now - earliest_time.replace(tzinfo=None)
    
    # Apply offset to all events
    for stage in timeline:
        for event in stage.get('events', []):
            if 'TimeCreated' in event:
                original_time = parse_timestamp(event['TimeCreated'])
                new_time = original_time.replace(tzinfo=None) + time_offset
                event['TimeCreated'] = new_time.isoformat() + "Z"
                event['@timestamp'] = new_time.isoformat() + "Z"  # For Elastic
    
    return timeline

def main():
    # Validate token is set
    if AUTH_TOKEN == 'YOUR_HEC_TOKEN_HERE':
        print("WARNING: SIEM_TOKEN not configured. Set the SIEM_TOKEN environment variable.")
        print("Example: export SIEM_TOKEN='your-hec-token-here'")
        # Continue anyway for dry-run testing
    
    if not os.path.exists(LOG_FILE):
        print(f"Error: Log file not found at {LOG_FILE}")
        sys.exit(1)

    print(f"Reading logs from: {LOG_FILE}")
    
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON log file: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Failed to read log file: {e}")
        sys.exit(1)

    timeline = data.get('timeline', [])
    if not timeline:
        print("Error: No 'timeline' key found in JSON or timeline is empty.")
        sys.exit(1)

    # Rebase timestamps to NOW while preserving relative intervals
    print("[*] Rebasing event timestamps to current time (preserving intervals)...")
    timeline = rebase_timestamps(timeline)
    
    print(f"[*] Starting replay to {INPUT_TYPE} at {SIEM_URL}...")
    
    success_count = 0
    fail_count = 0
    
    for stage in timeline:
        stage_name = stage.get('stage', 'Unknown Stage')
        print(f"\n--- Processing Stage: {stage_name} ---")
        
        events = stage.get('events', [])
        for event in events:
            if INPUT_TYPE == 'splunk':
                if send_to_splunk(event, SIEM_URL, AUTH_TOKEN):
                    success_count += 1
                else:
                    fail_count += 1
            elif INPUT_TYPE == 'elastic':
                if send_to_elastic(event, SIEM_URL, AUTH_TOKEN):
                    success_count += 1
                else:
                    fail_count += 1
            else:
                print(f"[-] Unknown SIEM type: {INPUT_TYPE}")
                fail_count += 1
            
            # Preserve original event timing by using realistic delays
            time.sleep(0.1)

    print(f"\n{'='*50}")
    print(f"Replay completed. Success: {success_count}, Failed: {fail_count}")
    if fail_count > 0:
        print("WARNING: Some events failed to send. Check SIEM connectivity and token.")
        sys.exit(1)

if __name__ == "__main__":
    main()

