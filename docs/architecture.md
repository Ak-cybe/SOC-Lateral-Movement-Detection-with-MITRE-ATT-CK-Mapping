# Detection Architecture & Data Flow

This document outlines the technical architecture for the Lateral Movement Detection project.

## High-Level Data Flow

```ascii
┌─────────────┐      ┌──────────┐      ┌─────────────┐
│   Windows   │─────>│ Winlogbeat│─────>│   Splunk    │
│   Endpoint  │ 4624 │   Agent   │ JSON │   Indexer   │
│  (DC, WKS)  │ 4625 │           │      │             │
└─────────────┘ 4672 └──────────┘      └──────┬──────┘
       │                                      │
       ▼                                      ▼
┌─────────────┐                        ┌─────────────────┐
│   Sysmon    │─────> (Optional) ────> │ Correlation Svc │
│  (Process)  │                        │ (Scheduled)     │
└─────────────┘                        └────────┬────────┘
                                                │
                                                ▼
                                       ┌─────────────────┐
                                       │  Alert Queue    │
                                       │  (Tier-1 Triage)│
                                       └─────────────────┘
```

## Component Breakdown

### 1. Data Collection (Endpoints)
- **Source:** Windows Security Events + Sysmon.
- **Critical Events:**
    - `4625`: Failed Logon (Brute Force Indicator).
    - `4624`: Successful Logon (Lateral Movement Indicator).
    - `4672`: Special Privileges Assigned (Context).
    - `Sysmon 1 `: Process Creation (`psexec`, `wsmprovhost`).
    - `Sysmon 3`: Network Connections (RDP/SMB).

### 2. Ingestion (Agents)
- **Splunk Universal Forwarder** or **Elastic Agent**.
- **Requirement:** Must parse fields `Source_Network_Address` and `Account_Name`.

### 3. Correlation Engine
- **Splunk:** Runs scheduled SPL searches every 5-15 minutes (`correlation-rules/splunk/`).
- **Elastic:** Runs detection rules continuously (`correlation-rules/elastic/`).
- **Logic:**
    - Aggregates events by `Account_Name` and `Source_Network_Address`.
    - Applies thresholds (e.g., >5 failures).
    - Checks against lookups (Exclusions).

### 4. Alerting
- Alerts are generated with calculated **Risk Scores**.
- Sent to SOAR or Ticket System via Webhook.
