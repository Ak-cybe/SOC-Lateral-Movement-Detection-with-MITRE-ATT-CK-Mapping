<div align="center">

  ![Banner](https://capsule-render.vercel.app/api?type=waving&color=0:FF0000,100:330000&height=180&section=header&text=SOC%20Lateral%20Movement&fontSize=50&fontColor=ffffff&fontAlignY=35&desc=Enterprise%20Defense%20Suite%20%7C%20Splunk%20%2B%20Elastic&descAlignY=60&descSize=20&animation=fadeIn)

  <br />

  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=F71E36&center=true&vCenter=true&width=600&lines=Detect+Brute+Force+Attacks;Stop+Lateral+Movement;Hunt+Privilege+Escalation;Map+to+MITRE+ATT%26CK" alt="Typing SVG" />

  <br />

  [![MITRE](https://img.shields.io/badge/MITRE%20ATT%26CK-T1110%20%7C%20T1021-red?style=for-the-badge&logo=target)](https://attack.mitre.org/)
  [![Splunk](https://img.shields.io/badge/Splunk-SPL-green?style=for-the-badge&logo=splunk)](https://splunk.com)
  [![Elastic](https://img.shields.io/badge/Elastic-KQL-blue?style=for-the-badge&logo=elastic)](https://elastic.co)
  [![Build](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge&logo=github)](https://github.com/)

</div>

---

## ⚡ Project Overview

**Stop attackers before they own your domain.**

This project is a **battle-tested detection capability** designed to identify the critical path of an intrusion: **Brute Force → Lateral Movement → Privilege Abuse**. relying on standard Windows logs, it builds a resilient detection mesh that identifies attacks even when they use legitimate tools like `psexec` or `RDP`.

> **💥 Why this matters:** Most SOCs only alert on "Failed Logins". This project connects the dots—alerting only when a user fails 20 times *and then* successfully hops to a critical server.

---

## 💀 Kill Chain Architecture

We track the adversary at every step of the movement phase.

```mermaid
graph LR
    A[🔓 Brute Force] -->|Phase 1| B[✅ Credential Access]
    B -->|Phase 2| C[🔀 Lateral Movement]
    C -->|Phase 3| D[👑 Domain Dominance]

    style A fill:#a80000,stroke:#333,stroke-width:2px,color:#fff
    style B fill:#e67e22,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#f1c40f,stroke:#333,stroke-width:2px,color:#000
    style D fill:#27ae60,stroke:#333,stroke-width:2px,color:#fff
```

### 🎯 Detection Coverage

| Tactic | Technique | Detection Logic | Severity |
|:--- |:--- |:--- |:---|
| **Credential Access** | **Password Spraying** | `Uniques > 10` & `Fails < 50` | 🟠 High |
| **Credential Access** | **Brute Force** | `Events > 5` in 5 mins + GeoIP | 🔴 Critical |
| **Lateral Movement** | **Remote Services** | `Hosts ≥ 3` via RDP/WinRM/SMB | 🔴 Critical |
| **Privilege Escalation** | **Valid Accounts** | Admin login + Anomalous Context | 🟡 Medium |

*Full mapping available in [MITRE Mapping Docs](investigation-playbook/mitre_attack_mapping.md).*

---

## 🛠️ Deployment & Usage

### 1. ⚙️ Prerequisites (Don't skip this)
Your detections are only as good as your logs. Apply these configs first:
*   📜 **[Windows Audit Policy](configs/windows_audit_policy.xml)** (Enable Logon/Logoff)
*   📜 **[Sysmon Configuration](configs/sysmon_config.xml)** (Targeting Lateral Movement Ports 445, 3389, 5985)

### 2. 🛡️ Deploy Rules
Populate the `lookups/` CSVs with your safe IPs, then:
*   **Splunk:** Copy `correlation-rules/splunk/*.spl` to your Search Head.
*   **Elastic:** Import `correlation-rules/elastic/*.json` to Kibana.

### 3. 🧪 Validate (Attack Simulation)
Don't guess. Test. Run the Python replay script to fire 50+ malicious logs into your SIEM and verify the alert triggers.

```bash
# Simulates a full attack scenario from Brute Force to Admin Access
python scripts/replay_attack_scenario.py
```

---

## 📂 Repository Structure

```tree
SOC-Lateral-Movement-Detection/
├── 📁 correlation-rules/   # The Brains (SPL & KQL)
├── 📁 configs/             # The Eyes (Sysmon & Audit)
├── 📁 docs/                # The Manuals (Architecture & Triage)
├── 📁 lookups/             # The Allow-lists
├── 📁 scripts/             # The Test Tools
└── 📄 README.md            # You are here
```

---

## 📚 Analyst Resources

*   **[Architecture Diagram](docs/architecture.md)** - How the data flows.
*   **[Severity Matrix](docs/severity_matrix.md)** - How we calculate Risk Scores.
*   **[Troubleshooting](docs/troubleshooting.md)** - Rule not firing? Check here.
*   **[Postmortem Report](docs/POSTMORTEM.md)** - Lessons learned from building this.

---

## 📸 Usage Gallery

### 1. Brute Force Alert (Splunk)
<p align="center">
  <img src="screenshots/brute_force_alert.png" alt="Brute Force Alert" width="90%"/>
</p>
<i>Splunk alert showing 20+ failed login attempts.</i>

### 2. Attack Path Visualization
<p align="center">
  <img src="screenshots/lateral_movement_attack_path.png" alt="Lateral Movement Attack Path" width="90%"/>
</p>

### 3. Elastic SIEM Dashboard
<p align="center">
  <img src="screenshots/elastic_dashboard.png" alt="Elastic Dashboard" width="90%"/>
</p>

---

## 📚 References & Credits

### Core Frameworks
*   [MITRE ATT&CK: T1110 (Brute Force)](https://attack.mitre.org/techniques/T1110/)
*   [MITRE ATT&CK: T1021 (Remote Services)](https://attack.mitre.org/techniques/T1021/)
*   [MITRE ATT&CK: T1078 (Valid Accounts)](https://attack.mitre.org/techniques/T1078/)

### Documentation
*   [Microsoft Event ID 4625](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625)
*   [Splunk Security Essentials](https://splunkbase.splunk.com/app/3435/)
*   [Elastic Detection Rules](https://www.elastic.co/guide/en/security/current/detection-engine-overview.html)

---

<div align="center">

**[ Report Bug ](https://github.com/Ak-cybe/SOC-Lateral-Movement-Detection/issues)** • **[ Request Feature ](https://github.com/Ak-cybe/SOC-Lateral-Movement-Detection/pulls)**

<img src="https://img.shields.io/github/stars/Ak-cybe/SOC-Lateral-Movement-Detection?style=social" alt="Stars"/>

</div>
