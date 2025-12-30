# Log Forwarding & Data Source Guide

This guide details the requirements to ensure logs successfully reach the SIEM for analysis using these detection rules.

## 1. Prerequisites Checklist
- [ ] **Windows Event Forwarding (WEF)** configured (or equivalent agent deployed)
- [ ] **Advanced Audit Policy** applied via GPO
- [ ] **Sysmon** installed and configured on all endpoints
- [ ] **NTP Synchronization** enabled (Time diff > 5 mins breaks correlation)
- [ ] **SIEM Indexer** receiving data in `winlogbeat-*` or `wineventlog` indices

## 2. Windows Audit Policy (Mandatory)
Apply the settings found in `configs/windows_audit_policy.xml`. Use `auditpol` to verify:

```cmd
auditpol /get /category:"Logon/Logoff"
```
**Expected Output:**
- Logon: Success and Failure
- Special Logon: Success and Failure

## 3. Sysmon Configuration
Deploy Sysmon to capture Process Creation (ID 1) and Network Connections (ID 3).
Use the provided config: `configs/sysmon_config.xml`

```cmd
sysmon64.exe -i configs\sysmon_config.xml
```

## 4. Required Log Fields
The detection rules *will fail* if these fields are missing or null. Ensure your ingestion pipeline (Logstash/Splunk UF) parses these correctly:

| Event ID | Critical Field | Purpose |
|----------|----------------|---------|
| 4625 | `Account_Name` | Identify target user |
| 4625 | `Source_Network_Address` | **MUST** be a valid IP (IPv4/IPv6). Null/Dash triggers false negatives. |
| 4624 | `Logon_Type` | Distinguish RDP (10) vs Network (3) |
| 4624 | `ComputerName` | Host identification |
| 4672 | `PrivilegeList` | Context for admin abuse |
| Sysmon 1 | `CommandLine` | Detect tool flags (e.g. psexec -s) |

## 5. Verification Query
Run this in your SIEM to verify data flow before deploying rules:

**Splunk:**
```spl
index=wineventlog EventCode=4624 Source_Network_Address!=* 
| stats count as "Valid Logs"
```

**Elastic:**
```json
GET winlogbeat-*/_count
{
  "query": {
    "exists": { "field": "source.ip" }
  }
}
```
If count is 0, **STOP**. Fix your forwarding agent configuration.
