# Validation Guide

This guide details how to validate the detection rules using the provided attack scenario logs.

## Prerequisites

- **Python 3.x** installed
- **Requests** library installed (`pip install requests`)
- Access to a **Splunk** instance (with HEC enabled) or **Elastic Stack**

## Validation Steps

1.  **Deploy Detection Rules**:
    -   Import `.spl` files into Splunk or `.json` rules into Elastic Security.
    -   Ensure the rules are enabled and scheduled.

2.  **Configure Replay Script**:
    -   Open `scripts/replay_attack_scenario.py`.
    -   Update the `SIEM_URL` and `AUTH_TOKEN` variables with your environment details.
    -   Select the target platform (`INPUT_TYPE = 'splunk'` or `'elastic'`).

3.  **Run the Replay**:
    ```bash
    python scripts/replay_attack_scenario.py
    ```
    This script reads `logs/attack_scenario_timeline.json` and pushes events to your SIEM.

4.  **Wait for Correlation**:
    -   Wait approximately **15 minutes**. This covers the maximum time window used in the correlation rules.

5.  **Verify Alerts**:
    -   Query your SIEM for triggered alerts.
    -   Compare the results against `tests/expected_alerts.json`.

6.  **Success Criteria**:
    -   [ ] Brute Force detected (Severity: Critical)
    -   [ ] Lateral Movement detected (Distinct hosts >= 3)
    -   [ ] Alert fields match expected values (Source IP: 192.168.1.105)

## Troubleshooting

-   **No Alerts?**
    -   Check SIEM ingestion logs to ensure events were received.
    -   Verify timestamp parsing (events might be too old if rule ignores historic data).
    -   Check `lookups` files are strictly populated.
