# 🗺️ MITRE ATT&CK Mapping

## Detection Coverage Matrix

This document maps the detection rules to MITRE ATT&CK techniques and provides coverage analysis.

---

## 📊 Technique Coverage

### Primary Techniques Detected

| Technique ID | Technique Name | Tactic | Detection Rule | Confidence |
|-------------|----------------|--------|----------------|------------|
| T1110 | Brute Force | Credential Access | `brute_force_detection.spl` | High |
| T1110.001 | Password Guessing | Credential Access | `brute_force_detection.spl` | High |
| T1078 | Valid Accounts | Initial Access / Persistence | `successful_login_after_bruteforce.spl` | High |
| T1021 | Remote Services | Lateral Movement | `lateral_movement_detection.spl` | Medium |
| T1021.001 | Remote Desktop Protocol | Lateral Movement | `lateral_movement_detection.spl` | Medium |
| T1021.002 | SMB/Windows Admin Shares | Lateral Movement | `lateral_movement_detection.spl` | Medium |
| T1078.002 | Domain Accounts | Privilege Escalation | `kill_chain_alert.spl` | High |

---

## 🔗 Attack Chain Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KILL CHAIN COVERAGE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TA0001: Initial Access                                                      │
│  └── T1078 Valid Accounts ──────────────[ successful_login_after_bf.spl ]   │
│                                                                              │
│  TA0006: Credential Access                                                   │
│  └── T1110 Brute Force ─────────────────[ brute_force_detection.spl ]       │
│      └── T1110.001 Password Guessing ───[ brute_force_detection.spl ]       │
│                                                                              │
│  TA0008: Lateral Movement                                                    │
│  └── T1021 Remote Services ─────────────[ lateral_movement_detection.spl ]  │
│      ├── T1021.001 RDP ─────────────────[ lateral_movement_detection.spl ]  │
│      └── T1021.002 SMB ─────────────────[ lateral_movement_detection.spl ]  │
│                                                                              │
│  TA0004: Privilege Escalation (Abuse)                                        │
│  └── T1078.002 Domain Accounts ─────────[ kill_chain_alert.spl ]            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📑 Detailed Technique Breakdown

### T1110 - Brute Force

| Attribute | Details |
|-----------|---------|
| **Detection Source** | Windows Security Event Log |
| **Event ID** | 4625 (Failed Logon) |
| **Key Fields** | Account_Name, Source_Network_Address, Logon_Type |
| **Detection Rule** | `brute_force_detection.spl` |
| **Threshold** | >5 failed attempts in 5 minutes |
| **Sub-techniques** | T1110.001 (Password Guessing), T1110.002 (Password Cracking), T1110.003 (Password Spraying) |

**MITRE Reference**: https://attack.mitre.org/techniques/T1110/

---

### T1078 - Valid Accounts

| Attribute | Details |
|-----------|---------|
| **Detection Source** | Windows Security Event Log |
| **Event ID** | 4624 (Successful Logon) after 4625 pattern |
| **Key Fields** | Account_Name, Source_Network_Address, Logon_Type |
| **Detection Rule** | `successful_login_after_bruteforce.spl` |
| **Correlation** | Success within 10 min after >5 failed attempts |
| **Sub-techniques** | T1078.002 (Domain Accounts) |

**MITRE Reference**: https://attack.mitre.org/techniques/T1078/

---

### T1021 - Remote Services

| Attribute | Details |
|-----------|---------|
| **Detection Source** | Windows Security Event Log |
| **Event ID** | 4624 (Logon Type 3, 10) |
| **Key Fields** | Account_Name, ComputerName, Source_Network_Address |
| **Detection Rule** | `lateral_movement_detection.spl` |
| **Threshold** | ≥3 distinct hosts in 10 minutes |
| **Sub-techniques** | T1021.001 (RDP), T1021.002 (SMB/Admin Shares) |

**MITRE Reference**: https://attack.mitre.org/techniques/T1021/

---

### T1078.002 - Domain Accounts

| Attribute | Details |
|-----------|---------|
| **Detection Source** | Windows Security Event Log |
| **Event ID** | 4672 (Special Privileges Assigned) |
| **Key Fields** | SubjectUserName, PrivilegeList |
| **Detection Rule** | `kill_chain_alert.spl` |
| **Context** | High-privilege logon following lateral movement |

**Note**: This is NOT privilege escalation via exploitation (T1068). EventID 4672 indicates administrative privilege assignment, which maps to privilege abuse under T1078.

**MITRE Reference**: https://attack.mitre.org/techniques/T1078/002/

---

## 📈 Coverage Gaps

### Techniques NOT Covered by This Project

| Technique ID | Technique Name | Why Not Covered |
|-------------|----------------|-----------------|
| T1068 | Exploitation for Privilege Escalation | Requires EDR/process telemetry |
| T1003 | OS Credential Dumping | Requires EDR/Sysmon |
| T1055 | Process Injection | Requires EDR/Sysmon |
| T1070 | Indicator Removal | Log deletion not monitored |
| T1059 | Command and Scripting Interpreter | Requires PowerShell logging |

**Recommended Additional Data Sources**:
- Sysmon (Process creation, network connections)
- PowerShell Script Block Logging
- EDR telemetry
- Network flow data

---

## 🎯 Detection Confidence Levels

| Level | Criteria | Rules |
|-------|----------|-------|
| **High** | Specific event + context | Brute Force, Success After BF |
| **Medium** | Behavioral pattern | Lateral Movement |
| **Low** | Anomaly-based | - |

---

## 📚 References

- [MITRE ATT&CK Matrix](https://attack.mitre.org/)
- [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [Windows Event Logging Cheat Sheet](https://www.malwarearchaeology.com/cheat-sheets)
