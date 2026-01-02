# 🔍 Brute Force Investigation Playbook

## Overview

| Field | Value |
|-------|-------|
| **Playbook ID** | SOC-PB-001 |
| **Author** | SOC Team |
| **Version** | 1.0 |
| **MITRE ATT&CK** | T1110 (Brute Force), T1110.001 (Password Guessing) |
| **Priority** | Medium → High (based on target account) |

---

## 🔗 Alert Enrichment (Auto-populated)

- **Alert Field: `source.ip`** → Matches **Playbook Step 2** (IP Reputation Check)
- **Alert Field: `user.name`** → Matches **Playbook Step 3** (Account Privilege Check)
- **Alert Field: `failed_attempts`** → Logic: If >20, treat as **Immediate Escalation**

## 🚨 Alert Trigger Criteria

- **Primary**: >5 failed login attempts (EventCode 4625) in 5 minutes from same source IP
- **Escalation**: >10 attempts = High, >20 attempts = Critical

---

## 📋 Triage Steps (Tier-1)

### Step 1: Validate Alert (2 min)
```
□ Confirm source IP address
□ Identify target account(s)
□ Check if account is privileged (admin, service account)
□ Verify timestamp and duration of attack
```

### Step 2: Source IP Analysis (3 min)
```
□ Check if IP is internal or external
□ If internal: Identify the workstation/user
□ If external: Check IP reputation (VirusTotal, AbuseIPDB)
□ Review recent activity from this IP
```

### Step 3: Target Account Analysis (3 min)
```
□ Is account active or disabled?
□ Check account lockout status
□ Review recent successful logins for this account
□ Identify account privilege level
```

---

## 🔬 Investigation Steps (Tier-2)

### Step 4: Attack Pattern Analysis (5 min)

**Splunk Query:**
```spl
index=wineventlog sourcetype=WinEventLog:Security EventCode=4625
  Source_Network_Address="<ATTACKER_IP>"
| stats count by Account_Name, ComputerName, Logon_Type
| sort - count
```

**Questions to Answer:**
- Single target or multiple accounts?
- Single host or multiple targets?
- What logon types? (Network=3, RDP=10)

### Step 5: Success Check (3 min)

**Critical**: Did brute force succeed?

```spl
index=wineventlog sourcetype=WinEventLog:Security 
  (EventCode=4624 OR EventCode=4625)
  Source_Network_Address="<ATTACKER_IP>"
| sort _time
| table _time, EventCode, Account_Name, ComputerName
```

- If 4624 appears after multiple 4625s → **ESCALATE IMMEDIATELY**

### Step 6: Lateral Movement Check (5 min)

If compromise detected:
```spl
index=wineventlog sourcetype=WinEventLog:Security EventCode=4624
  Account_Name="<COMPROMISED_ACCOUNT>"
| stats dc(ComputerName) as hosts_accessed values(ComputerName) as targets
  by Source_Network_Address
| where hosts_accessed > 2
```

---

## 🛡️ Containment Actions

| Action | When to Apply | Who Executes |
|--------|---------------|--------------|
| Block source IP at firewall | External IP, confirmed malicious | SOC / Network Team |
| Disable compromised account | Success after brute force | SOC Tier-2 + Identity Team |
| Isolate source workstation | Internal IP, confirmed compromise | SOC + Endpoint Team |
| Force password reset | Account targeted but not compromised | Identity Team |

---

## 📊 Evidence Collection Checklist

```
□ Screenshot of alert with timestamps
□ Source IP details and reputation check
□ List of targeted accounts
□ Timeline of failed/successful logins
□ Related alerts (lateral movement, privilege escalation)
□ Network logs showing connection attempts
```

---

## 📝 Documentation Requirements

| Field | Example |
|-------|---------|
| Alert Time | 2025-12-28 14:30:01 UTC |
| Source IP | 192.168.1.105 |
| Target Account(s) | admin.service |
| Attack Duration | 53 seconds |
| Failed Attempts | 20 |
| Success Detected | Yes/No |
| Containment Actions | Account disabled, IP blocked |
| Ticket ID | INC-2024-12345 |

---

## ⏱️ SLA Requirements

| Severity | Initial Triage | Investigation Complete | Containment |
|----------|----------------|------------------------|-------------|
| Medium | 15 min | 1 hour | 2 hours |
| High | 10 min | 30 min | 1 hour |
| Critical | 5 min | 15 min | 30 min |

---

## 📚 References

- [Windows Event 4625 Documentation](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625)
- [MITRE ATT&CK T1110](https://attack.mitre.org/techniques/T1110/)
- [NIST SP 800-61 Incident Handling Guide](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf)
