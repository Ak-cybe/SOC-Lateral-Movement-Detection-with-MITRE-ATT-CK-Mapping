# Severity Scoring Matrix

This document defines the standard logic for calculating alert severity for Brute Force and Lateral Movement detections.

## 🧮 Brute Force Risk Scoring

**Formula:**
`Risk Score = (Attempt Count Score) + (Privilege Score) + (Success Outcome Score)`

| Factor | Weight | Condition | Score |
|--------|--------|-----------|-------|
| **Failed Attempts** | 30% | > 5 attempts | +15 |
| | | > 10 attempts | +25 |
| | | > 20 attempts | +35 |
| **Target Account** | 40% | Standard User | +10 |
| | | Service Account | +25 |
| | | Admin / Domain Admin | +40 |
| **Outcome** | 30% | Failed Only | +0 |
| | | Successful Login Detected | +30 |

### Severity Levels

| Total Score | Severity Label | SLA (Triage) |
|-------------|----------------|--------------|
| 0 - 39 | **Low** | 24 hours |
| 40 - 69 | **Medium** | 4 hours |
| 70 - 89 | **High** | 1 hour |
| 90 - 100+ | **Critical** | 15 minutes |

### Example Calculation
*Scenario: Attacker tries 25 times to login as 'admin', failure only.*
- Attempts (>20): **+35**
- Account (Admin): **+40**
- Outcome (Fail): **+0**
- **Total:** 75 (**High**)

---

## 🚀 Lateral Movement Risk Scoring

**Formula:**
`Risk Score = (Host Count Score) + (Protocol Score) + (Velocity Score)`

| Factor | Weight | Condition | Score |
|--------|--------|-----------|-------|
| **Host Count** | 40% | 3-5 hosts | +20 |
| | | 6-10 hosts | +30 |
| | | > 10 hosts | +40 |
| **Protocol** | 30% | RDP (Standard) | +10 |
| | | SMB/WinRM (Cmd Line) | +25 |
| | | PsExec (Tool) | +30 |
| **Velocity** | 30% | > 1 host/min | +30 |
| | | < 1 host/min | +10 |

### Example Calculation
*Scenario: User accesses 4 hosts via PsExec in 2 minutes.*
- Hosts (3-5): **+20**
- Protocol (PsExec): **+30**
- Velocity (2 hosts/min): **+30**
- **Total:** 80 (**High**)
