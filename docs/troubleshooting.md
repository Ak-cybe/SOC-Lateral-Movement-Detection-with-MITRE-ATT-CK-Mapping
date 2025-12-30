# Troubleshooting Guide

Use this guide to resolve common issues where alerts fail to trigger or generate excessive noise.

## 🚨 Issue 1: Brute Force Alerts Not Triggering

**Symptoms:**
- Attack simulation runs, but no alert appears in the dashboard.

**Diagnosis Steps:**
1.  **Verify Raw Data:**
    -   Run: `index=wineventlog EventCode=4625 | stats count`
    -   *If count is 0:* Log forwarding is broken. Check Winlogbeat/Splunk UF.
2.  **Check IP Fields:**
    -   Run: `index=wineventlog EventCode=4625 | table Source_Network_Address`
    -   *If fields are null:* Your inputs.conf or parsing configuration is incorrect. The rule requires a valid IP.
3.  **Check Lookups:**
    -   Ensure the user/IP is not in `lookups/admin_jump_servers.csv` (if you are testing from an admin IP).

## ⚠️ Issue 2: Lateral Movement False Positives

**Symptoms:**
- Valid admin activity is triggering "Lateral Movement" alerts.

**Diagnosis Steps:**
1.  **Check Threshold:**
    -   Default rule triggers on **3 distinct hosts**. For large environments, increase this to **5**.
    -   Edit `lateral_movement_detection.spl`: `| where distinct_hosts >= 5`
2.  **Verify Exclusions:**
    -   Are your Jump Servers listed in `lookups/admin_jump_servers.csv`?
    -   Are your scanners (Nessus/Qualys) listed in `lookups/service_accounts.csv`?

## 📉 Issue 3: Missing Fields in Alerts

**Symptoms:**
- Alert fires but says "User: null" or "Source: unknown".

**Fix:**
- **Splunk:** Ensure `fieldalias` is configured if using non-standard sourcetypes.
- **Elastic:** Ensure ECS mapping is applied (`user.name`, `source.ip`).

## 🛠️ Debug Mode

To see what the rule *is* seeing (without filtering):
1.  Open the SPL file.
2.  Remove `| where ...` clauses.
3.  Run the search to see statistical baselines.
