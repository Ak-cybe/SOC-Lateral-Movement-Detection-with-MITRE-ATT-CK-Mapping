<div align="center">

  ![Banner](https://capsule-render.vercel.app/api?type=waving&color=0:FF0000,100:330000&height=180&section=header&text=SOC%20Lateral%20Movement&fontSize=50&fontColor=ffffff&fontAlignY=35&desc=Enterprise%20Defense%20Suite%20%7C%20Splunk%20%2B%20Elastic&descAlignY=60&descSize=20&animation=fadeIn)

  <br />

  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=F71E36&center=true&vCenter=true&width=600&lines=Detect+Brute+Force+Attacks;Stop+Lateral+Movement;Hunt+Privilege+Escalation;Map+to+MITRE+ATT%26CK" alt="Typing SVG" />

  <br />

  [![MITRE](https://img.shields.io/badge/MITRE%20ATT%26CK-T1110%20%7C%20T1021%20%7C%20T1078-red?style=for-the-badge&logo=target)](https://attack.mitre.org/)
  [![Splunk](https://img.shields.io/badge/Splunk-SPL-green?style=for-the-badge&logo=splunk)](https://splunk.com)
  [![Elastic](https://img.shields.io/badge/Elastic-KQL%2FEQL-blue?style=for-the-badge&logo=elastic)](https://elastic.co)
  [![Build](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge&logo=github)](https://github.com/)

</div>

---

## ⚡ Project Overview

**Stop attackers before they own your domain.**

This project is a **battle-tested detection capability** designed to identify the critical path of an intrusion: **Brute Force → Lateral Movement → Privilege Abuse**. Relying on standard Windows logs, it builds a resilient detection mesh that identifies attacks even when they use legitimate tools like `psexec` or `RDP`.

> **💥 Why this matters:** Most SOCs only alert on "Failed Logins". This project connects the dots—alerting only when a user fails 20 times *and then* successfully hops to a critical server.

---

## 🎯 What's Included

| Component | Description | Count |
|-----------|-------------|-------|
| **Splunk Detection Rules** | SPL correlation rules for all attack phases | 5 rules |
| **Elastic Detection Rules** | KQL/EQL rules with MITRE mapping | 5 rules |
| **Investigation Playbooks** | Step-by-step analyst response guides | 4 playbooks |
| **Incident Report Templates** | Standardized documentation templates | 2 templates |
| **Telemetry Configs** | Sysmon + Windows Audit Policy | 2 configs |
| **Validation Framework** | Scripts + sample logs for testing | Complete |
| **Lab Practice Guide** | Hands-on attack simulation guide | Detailed |

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

---

## 📊 MITRE ATT&CK Coverage

| Technique ID | Technique Name | Tactic | Detection | Data Source |
|-------------|----------------|--------|-----------|-------------|
| **T1110** | Brute Force | Credential Access | ✅ Splunk + Elastic | Event 4625 |
| **T1110.001** | Password Guessing | Credential Access | ✅ Splunk + Elastic | Event 4625 |
| **T1110.003** | Password Spraying | Credential Access | ✅ Splunk + Elastic | Event 4625 |
| **T1078** | Valid Accounts | Initial Access | ✅ Splunk + Elastic | Event 4624 |
| **T1021** | Remote Services | Lateral Movement | ✅ Splunk + Elastic | Event 4624 |
| **T1021.001** | RDP | Lateral Movement | ✅ Splunk + Elastic | Event 4624 (Type 10) |
| **T1021.002** | SMB/Admin Shares | Lateral Movement | ✅ Splunk + Elastic | Event 4624 (Type 3) |
| **T1078.002** | Domain Accounts | Privilege Escalation | ✅ Splunk + Elastic | Event 4672 |

*Full mapping available in [MITRE Mapping Docs](investigation-playbook/mitre_attack_mapping.md).*

---

## 🛠️ Prerequisites

### Required Software
- **SIEM**: Splunk Enterprise (8.x+) OR Elastic Stack (8.x+)
- **Python**: 3.8+ (for validation scripts)
- **pip packages**: `requests` (`pip install requests`)

### Required Data Sources
| Event ID | Description | Log Source | Required |
|----------|-------------|------------|----------|
| 4624 | Successful Logon | Windows Security | ✅ Yes |
| 4625 | Failed Logon | Windows Security | ✅ Yes |
| 4672 | Special Privileges Assigned | Windows Security | ✅ Yes |
| Sysmon 1 | Process Creation | Sysmon | 🟡 Recommended |
| Sysmon 3 | Network Connection | Sysmon | 🟡 Recommended |

### Telemetry Configuration
Apply these configs before deploying detections:
- 📜 **[Windows Audit Policy](configs/windows_audit_policy.xml)** - Enable Logon/Logoff auditing
- 📜 **[Sysmon Configuration](configs/sysmon_config.xml)** - Target lateral movement ports

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Ak-cybe/SOC-Lateral-Movement-Detection.git
cd SOC-Lateral-Movement-Detection
```

### 2. Configure Exclusion Lists
Edit the CSV files in `lookups/` to match your environment:
```
lookups/
├── admin_jump_servers.csv    # IT jump server IPs
├── service_accounts.csv      # Automation/service accounts
└── it_automation_accounts.csv # CI/CD and tool accounts
```

### 3. Deploy Rules
**Splunk:**
```bash
# Copy SPL files to Splunk Search Head
cp correlation-rules/splunk/*.spl $SPLUNK_HOME/etc/apps/search/local/savedsearches/
```

**Elastic:**
```bash
# Import via Kibana Detection Rules API or UI
# Navigate to Security → Detections → Manage rules → Import
```

### 4. Validate Deployment
```bash
# Set environment variables
export SIEM_URL="http://localhost:8088/services/collector/event"
export SIEM_TOKEN="YOUR_HEC_TOKEN"
export SIEM_TYPE="splunk"  # or "elastic"

# Run validation
python scripts/replay_attack_scenario.py
```

Expected output: Alerts matching `tests/expected_alerts.json`

---

## 📂 Repository Structure

```tree
SOC-Lateral-Movement-Detection/
├── 📁 correlation-rules/       # Detection Rules
│   ├── splunk/                 # 5 SPL rules
│   └── elastic/                # 5 JSON rules
├── 📁 configs/                 # Telemetry Configs
│   ├── sysmon_config.xml
│   └── windows_audit_policy.xml
├── 📁 investigation-playbook/  # Analyst Playbooks
│   ├── brute_force_playbook.md
│   ├── lateral_movement_playbook.md
│   ├── false_positive_handling.md
│   └── mitre_attack_mapping.md
├── 📁 incident-report/         # Report Templates
├── 📁 lookups/                 # Exclusion Lists (CSV)
├── 📁 logs/                    # Sample Attack Logs
├── 📁 scripts/                 # Validation Tools
├── 📁 tests/                   # Expected Outputs
├── 📁 docs/                    # Documentation
├── 📁 screenshots/             # UI Screenshots
└── 📄 PRACTICE_LAB_GUIDE.md   # Hands-on Lab Setup
```

---

## 🧪 How to Demo (5-Step Guide)

1. **Set up a test lab** - Follow [PRACTICE_LAB_GUIDE.md](PRACTICE_LAB_GUIDE.md)
2. **Deploy telemetry** - Apply Sysmon + Audit Policy configs
3. **Import detection rules** - Load SPL/JSON rules into your SIEM
4. **Run attack simulation** - Execute `python scripts/replay_attack_scenario.py`
5. **Verify alerts** - Confirm detection fires with correct severity and MITRE mapping

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Architecture Diagram](docs/architecture.md) | Data flow and component breakdown |
| [Severity Matrix](docs/severity_matrix.md) | Risk score calculation formulas |
| [Troubleshooting](docs/troubleshooting.md) | Common issues and fixes |
| [Validation Guide](docs/validation_guide.md) | Testing procedures |
| [Detection Engineering Notes](docs/DETECTION_ENGINEERING_NOTES.md) | FP tuning and maintenance |
| [Log Forwarding Guide](docs/log_forwarding_guide.md) | Data source requirements |

---

## 📸 Screenshots

<details>
<summary>Click to expand screenshots</summary>

### Brute Force Alert (Splunk)
<p align="center">
  <img src="screenshots/brute_force_alert.png" alt="Brute Force Alert" width="90%"/>
</p>

### Attack Path Visualization
<p align="center">
  <img src="screenshots/lateral_movement_attack_path.png" alt="Lateral Movement Attack Path" width="90%"/>
</p>

### Elastic SIEM Dashboard
<p align="center">
  <img src="screenshots/elastic_dashboard.png" alt="Elastic Dashboard" width="90%"/>
</p>

</details>

---

## �️ Roadmap

### ✅ Completed (v1.0)
- [x] Splunk detection rules (5 rules)
- [x] Elastic detection rules (5 rules)
- [x] Investigation playbooks
- [x] MITRE ATT&CK mapping
- [x] Validation framework
- [x] Practice lab guide

### 🔄 In Progress (v1.1)
- [ ] Sigma rule conversion for portability
- [ ] Jupyter notebook for Tier-3 analysis
- [ ] Baseline analysis automation

### 📋 Planned (v2.0)
- [ ] Grafana dashboard for alert metrics
- [ ] Threat intel feed integration (AbuseIPDB)
- [ ] SOAR playbook templates (Cortex XSOAR, Splunk SOAR)
- [ ] Machine learning anomaly detection

---

## 📚 References

### Core Frameworks
- [MITRE ATT&CK: T1110 (Brute Force)](https://attack.mitre.org/techniques/T1110/)
- [MITRE ATT&CK: T1021 (Remote Services)](https://attack.mitre.org/techniques/T1021/)
- [MITRE ATT&CK: T1078 (Valid Accounts)](https://attack.mitre.org/techniques/T1078/)

### Documentation
- [Microsoft Event ID 4625](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625)
- [Splunk Security Essentials](https://splunkbase.splunk.com/app/3435/)
- [Elastic Detection Rules](https://www.elastic.co/guide/en/security/current/detection-engine-overview.html)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[ Report Bug ](https://github.com/Ak-cybe/SOC-Lateral-Movement-Detection/issues)** • **[ Request Feature ](https://github.com/Ak-cybe/SOC-Lateral-Movement-Detection/pulls)**

<img src="https://img.shields.io/github/stars/Ak-cybe/SOC-Lateral-Movement-Detection?style=social" alt="Stars"/>

**Made with 🛡️ by [Amresh Kumar](https://github.com/Ak-cybe)**

</div>
