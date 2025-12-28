<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff0000,50:ff6b6b,100:4d96ff&height=200&section=header&text=SOC%20DETECT&fontSize=80&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Multi-Stage%20Brute%20Force%20%2B%20Lateral%20Movement%20Detection&descAlignY=55&descSize=20" width="100%"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=FF6B6B&center=true&vCenter=true&multiline=true&repeat=true&width=800&height=100&lines=%F0%9F%9B%A1%EF%B8%8F+Enterprise+SIEM+Correlation+Rules;%F0%9F%94%93+Brute+Force+%E2%86%92+Lateral+Movement+%E2%86%92+Privilege+Abuse;%F0%9F%8E%AF+MITRE+ATT%26CK+T1110+%7C+T1021+%7C+T1078" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/MITRE%20ATT%26CK-T1110%20|%20T1021%20|%20T1078-ff0000?style=for-the-badge&logo=target&logoColor=white" alt="MITRE"/>
  <img src="https://img.shields.io/badge/Splunk-SPL-00C853?style=for-the-badge&logo=splunk&logoColor=white" alt="Splunk"/>
  <img src="https://img.shields.io/badge/Elastic-SIEM-005571?style=for-the-badge&logo=elastic&logoColor=white" alt="Elastic"/>
  <img src="https://img.shields.io/badge/Windows-Security%20Logs-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/Ak-cybe/SOC-Lateral-Movement-Detection?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/Ak-cybe/SOC-Lateral-Movement-Detection?style=social" alt="Forks"/>
  <img src="https://img.shields.io/github/license/Ak-cybe/SOC-Lateral-Movement-Detection?color=blue" alt="License"/>
  <img src="https://komarev.com/ghpvc/?username=Ak-cybe&label=Profile%20Views&color=ff6b6b&style=flat" alt="Views"/>
</p>

---

## 🎯 About This Project

<img align="right" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjRxY2VqNWF5NzJnN2I5aHFnOTVsMnlvbDVmZGptN2R5MnNpOXFnaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPEqDGUULpEU0aQ/giphy.gif" width="300"/>

This project implements **multi-stage attack detection** using SIEM correlation rules. It detects the complete attack chain from initial brute force attempts through credential compromise to lateral movement across internal systems.

> [!IMPORTANT]
> This project detects **privilege abuse via administrative logons**, not vulnerability-based privilege escalation. EventID 4672 indicates high-privilege logon assignment, not exploitation.

### 🔥 Detection Capabilities

| Stage | Event ID | Detection | MITRE Technique |
|-------|----------|-----------|-----------------|
| 1️⃣ Brute Force | 4625 | Failed login threshold | T1110 |
| 2️⃣ Credential Compromise | 4624 | Success after brute force | T1078 |
| 3️⃣ Lateral Movement | 4624 | Multi-host authentication | T1021 |
| 4️⃣ Privilege Abuse | 4672 | High-privilege logon | T1078.002 |

### 🔀 Attack Path Visualization
<p align="center">
  <img src="screenshots/lateral_movement_attack_path.png" alt="Lateral Movement Attack Path" width="85%"/>
</p>
<p align="center"><i>Attack path showing malicious nodes (red), expected behaviors (green), and rare activities (yellow)</i></p>

<br clear="right"/>

---

## ⚡ Attack Chain Flow

```mermaid
flowchart LR
    A[🔓 Brute Force<br/>EventID 4625<br/>T1110] --> B[✅ Success<br/>EventID 4624<br/>T1078]
    B --> C[🔀 Lateral Movement<br/>Multi-Host Auth<br/>T1021]
    C --> D[👑 Privilege Abuse<br/>EventID 4672<br/>T1078.002]
    
    style A fill:#ff6b6b,color:#fff
    style B fill:#ffd93d,color:#000
    style C fill:#6bcb77,color:#fff
    style D fill:#4d96ff,color:#fff
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700"/>
</p>

### 🏗️ SIEM Detection Architecture

<p align="center">
  <img src="screenshots/siem_kill_chain_flow.png" alt="SIEM Kill Chain Architecture" width="95%"/>
</p>
<p align="center"><i>SIEM Kill Chain Flow: Rule-based IDS → Network Monitoring → Anomaly Detection → Alert & Mitigate</i></p>

---

## 📂 Repository Structure

```
SOC-Lateral-Movement-Detection/
├── 📁 correlation-rules/
│   ├── 📁 splunk/
│   │   ├── brute_force_detection.spl
│   │   ├── successful_login_after_bruteforce.spl
│   │   ├── lateral_movement_detection.spl
│   │   └── kill_chain_alert.spl
│   └── 📁 elastic/
│       ├── brute_force_detection.json
│       ├── successful_login_detection.json
│       └── lateral_movement_detection.json
├── 📁 logs/
│   ├── windows_security_4625_failed_logins.json
│   ├── windows_security_4624_successful_logins.json
│   ├── windows_security_4672_privilege_assigned.json
│   └── attack_scenario_timeline.json
├── 📁 investigation-playbook/
│   ├── brute_force_playbook.md
│   ├── lateral_movement_playbook.md
│   ├── false_positive_handling.md
│   └── mitre_attack_mapping.md
├── 📁 incident-report/
│   ├── incident_report_template.md
│   └── sample_incident_report.md
└── 📄 README.md
```

---

## 🛠️ Detection Logic

<img align="right" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnF5ZnJwcXk2cTh4MHgxdnFpbXo2aDFqOHRhbmRmMG1ocGVrMjBnOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tn33aiTi1jkl6H6/giphy.gif" width="280"/>

### Brute Force Detection (Splunk SPL)
```spl
index=wineventlog sourcetype=WinEventLog:Security EventCode=4625
| bin _time span=5m
| stats count as failed_attempts dc(ComputerName) as target_hosts 
  values(ComputerName) as targets by Account_Name, Source_Network_Address, _time
| where failed_attempts > 5
| eval severity=case(failed_attempts>20, "Critical", failed_attempts>10, "High", true(), "Medium")
```

### Lateral Movement Conditions
```
User authenticates to ≥3 distinct internal hosts
├── Within 10-minute time window
├── From same source IP (non-admin workstation)
└── Outside normal admin patterns
    ├── Excluded: Jump servers
    ├── Excluded: IT automation accounts
    └── Excluded: Service accounts
```

<br clear="right"/>

---

## 🎭 SOC Analyst Responsibilities Simulated

| Tier | Responsibility | Artifacts |
|------|----------------|-----------|
| **Tier-1** | Alert monitoring & triage | Correlation rules |
| **Tier-2** | Correlation analysis & investigation | Investigation playbooks |
| **Incident Response** | Documentation & remediation | Incident reports |

### 🔧 Elastic Security - Detection Rules
<p align="center">
  <img src="screenshots/elastic_detection_rules.png" alt="Elastic Detection Rules" width="95%"/>
</p>
<p align="center"><i>337+ detection rules with risk scoring, severity levels, and continuous monitoring</i></p>

---

## 🗺️ MITRE ATT&CK Mapping

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcTl5eWd2Y3FqYWFuaXJocGF0YTd6bWNhNWF4anEwc2xnczd6bnNrbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/077i6AULCXc0FKTj9s/giphy.gif" width="600"/>
</p>

| Technique ID | Technique Name | Detection Rule |
|-------------|----------------|----------------|
| T1110 | Brute Force | `brute_force_detection.spl` |
| T1110.001 | Password Guessing | `brute_force_detection.spl` |
| T1078 | Valid Accounts | `successful_login_after_bruteforce.spl` |
| T1021 | Remote Services | `lateral_movement_detection.spl` |
| T1078.002 | Domain Accounts | `kill_chain_alert.spl` |

---

## ⚠️ Assumptions & Limitations

- **Assumes** Windows Security auditing is enabled (Audit Logon Events)
- **Does not detect** kernel-level or vulnerability-based privilege escalation
- **Relies on** log integrity and proper forwarding to SIEM
- **Requires** tuning thresholds based on environment baseline
- **Elastic rules** use cumulative risk scoring across attack stages

---

## 🚀 Quick Start

### Splunk Import
```bash
# Copy SPL files to Splunk saved searches
cp correlation-rules/splunk/*.spl $SPLUNK_HOME/etc/apps/search/local/savedsearches.conf
```

### Elastic Import
```bash
# Import detection rules via Kibana API
curl -X POST "localhost:5601/api/detection_engine/rules/_import" \
  -H "kbn-xsrf: true" \
  -F file=@correlation-rules/elastic/brute_force_detection.json
```

---

## 📸 Screenshots

### � Brute Force Detection Alert
<p align="center">
  <img src="screenshots/brute_force_alert.png" alt="Brute Force Alert" width="90%"/>
</p>
<p align="center"><i>Splunk alert showing 20+ failed login attempts from attacker IP</i></p>

### ⏱️ Kill Chain Timeline
<p align="center">
  <img src="screenshots/kill_chain_timeline.png" alt="Kill Chain Timeline" width="90%"/>
</p>
<p align="center"><i>Multi-stage attack correlation: Brute Force → Success → Lateral → Privilege Abuse</i></p>

### 🔀 Lateral Movement Visualization
<p align="center">
  <img src="screenshots/lateral_movement.png" alt="Lateral Movement" width="90%"/>
</p>
<p align="center"><i>Network graph showing attacker movement across 6 internal hosts</i></p>

### 📊 Elastic SIEM Dashboard
<p align="center">
  <img src="screenshots/elastic_dashboard.png" alt="Elastic Dashboard" width="90%"/>
</p>
<p align="center"><i>Risk score accumulation and detection alerts in Elastic Security</i></p>

### 🎯 Splunk Enterprise Security - Incident Review
<p align="center">
  <img src="screenshots/splunk_incident_review.png" alt="Splunk Incident Review" width="95%"/>
</p>
<p align="center"><i>Real-time notable events with risk scores, urgency levels, and security domain classification</i></p>

---

## 📚 References

### MITRE ATT&CK Framework
- [MITRE ATT&CK: Brute Force (T1110)](https://attack.mitre.org/techniques/T1110/)
- [MITRE ATT&CK: Remote Services (T1021)](https://attack.mitre.org/techniques/T1021/)
- [MITRE ATT&CK: Valid Accounts (T1078)](https://attack.mitre.org/techniques/T1078/)
- [MITRE ATT&CK: Domain Accounts (T1078.002)](https://attack.mitre.org/techniques/T1078/002/)

### Windows Security Events
- [Event 4625 - Failed Logon](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625)
- [Event 4624 - Successful Logon](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624)
- [Event 4672 - Special Privileges Assigned](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672)

### SIEM Documentation
- [Splunk Security Essentials](https://splunkbase.splunk.com/app/3435/)
- [Elastic Security Detection Rules](https://www.elastic.co/guide/en/security/current/detection-engine-overview.html)
- [SANS Windows Security Log Encyclopedia](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/)

### Incident Response
- [NIST SP 800-61: Computer Security Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [SANS Incident Handler's Handbook](https://www.sans.org/white-papers/33901/)


---

## 👤 Author

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2Fib3Jrd3NraTJiNzdhdjd6OWFxY2s1Y3RheHJnc2psZmt4bnpjZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hqU2KkjW5bE2v2Z7Q2/giphy.gif" width="150"/>
</p>

<p align="center">
  <b>Amresh Kumar</b><br/>
  <i>SOC Analyst | Security Researcher | Red Team Enthusiast</i>
</p>

<p align="center">
  <a href="https://github.com/Ak-cybe">
    <img src="https://img.shields.io/badge/GitHub-Ak--cybe-181717?style=for-the-badge&logo=github" alt="GitHub"/>
  </a>
  <a href="https://linkedin.com/in/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn"/>
  </a>
</p>

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff0000,50:ff6b6b,100:4d96ff&height=120&section=footer" width="100%"/>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=18&duration=2000&pause=1000&color=FF6B6B&center=true&vCenter=true&width=500&lines=%F0%9F%94%90+Built+for+SOC+Analysts%2C+by+SOC+Analysts+%F0%9F%94%90" alt="Footer" />
</p>
