import argparse
import csv
import json
from collections import defaultdict
from statistics import mean, stdev

# Configuration
THRESHOLD_MULTIPLIER = 1.5
MIN_EVENTS_FOR_BASELINE = 10

def analyze_baseline(input_file, output_file):
    """
    Reads a CSV of authentication logs and establishes a 'Normal' baseline.
    Expects CSV columns: timestamp, user, source_ip, host
    """
    print(f"[+] Reading logs from {input_file}...")
    
    # Data structure: user -> date -> set(hosts)
    user_activity = defaultdict(lambda: defaultdict(set))
    
    try:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = row.get('user') or row.get('Account_Name')
                host = row.get('host') or row.get('ComputerName')
                # Simplistic date parsing (adjust format as needed)
                timestamp = row.get('timestamp') or row.get('_time')
                date = timestamp.split('T')[0] if 'T' in timestamp else timestamp.split(' ')[0]
                
                if user and host:
                    user_activity[user][date].add(host)
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return

    print("[+] Calculating baselines...")
    results = []
    
    for user, daily_data in user_activity.items():
        # Count distinct hosts accessed per day
        daily_host_counts = [len(hosts) for hosts in daily_data.values()]
        
        if len(daily_host_counts) < MIN_EVENTS_FOR_BASELINE:
            # Not enough data for reliable baseline
            continue
            
        avg_hosts = mean(daily_host_counts)
        max_hosts = max(daily_host_counts)
        # Use simple max-multiplier or std-dev if variance exists
        suggested_threshold = int(max_hosts * THRESHOLD_MULTIPLIER)
        
        results.append({
            'user': user,
            'days_active': len(daily_host_counts),
            'avg_hosts_per_day': round(avg_hosts, 1),
            'max_hosts_per_day': max_hosts,
            'suggested_alert_threshold': max(suggested_threshold, 3) # Floor at 3
        })
        
    print(f"[+] Writing analysis to {output_file}...")
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['user', 'days_active', 'avg_hosts_per_day', 'max_hosts_per_day', 'suggested_alert_threshold']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Lateral Movement Baselines")
    parser.add_argument("--input", required=True, help="Path to CSV logs (must have user, host, timestamp)")
    parser.add_argument("--output", default="baseline_report.csv", help="Output report path")
    args = parser.parse_args()
    
    analyze_baseline(args.input, args.output)
