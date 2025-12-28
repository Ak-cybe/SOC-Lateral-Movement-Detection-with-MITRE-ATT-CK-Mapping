# 🔀 Lateral Movement Investigation Playbook

## Overview

| Field | Value |
|-------|-------|
| **Playbook ID** | SOC-PB-002 |
| **Author** | SOC Team |
| **Version** | 1.0 |
| **MITRE ATT&CK** | T1021 (Remote Services), T1021.001 (RDP), T1021.002 (SMB) |
| **Priority** | High → Critical |

---

## 🚨 Alert Trigger Criteria

- **Primary**: Same user authenticates to ≥3 distinct hosts within 10 minutes
- **Conditions**: Same source IP, non-admin workstation, outside normal patterns
- **Escalation**: Access to critical assets (DC, file servers, databases)

---

## 📋 Triage Steps (Tier-1)

### Step 1: Validate Alert (2 min)
```
□ Confirm user account involved
□ List all target hosts accessed
□ Verify source IP is consistent
□ Check time window of activity
□ Is this a known admin or IT user?
```

### Step 2: User Context (3 min)
```
□ Identify user's role and department
□ Check user's normal access patterns
□ Is this behavior expected? (IT admin, help desk)
□ Verify user is currently working (not on leave, not terminated)
```

### Step 3: Quick Win Checks (2 min)
```
□ Is source IP a known jump server? → Exclude
□ Is account a service account? → Verify with IT
□ Is this during maintenance window? → Verify change ticket
□ Contact user for verification (if available)
```

---

## 🔬 Investigation Steps (Tier-2)

### Step 4: Full Access Analysis (5 min)

**Splunk Query - All Hosts Accessed:**
```spl
index=wineventlog sourcetype=WinEventLog:Security EventCode=4624
  Account_Name="<SUSPECT_USER>"
  earliest=-24h
| stats count earliest(_time) as first_access latest(_time) as last_access
  by ComputerName, Source_Network_Address, Logon_Type
| sort first_access
```

**Map the Movement:**
- Create timeline of all hosts accessed
- Identify critical/sensitive systems
- Note any deviation from baseline

### Step 5: Process Execution Analysis (10 min)

**On Each Target Host, Check:**
```spl
index=wineventlog sourcetype=WinEventLog:Security EventCode=4688
  Account_Name="<SUSPECT_USER>"
  ComputerName="<TARGET_HOST>"
| table _time, New_Process_Name, Process_Command_Line, Parent_Process_Name
| sort _time
```

**Look For:**
- Reconnaissance tools (net.exe, nltest.exe, ping.exe)
- Data collection (robocopy.exe, 7z.exe, rar.exe)
- Remote execution (psexec.exe, wmic.exe, powershell.exe)
- Credential access (mimikatz, procdump)

### Step 6: Data Exfiltration Check (5 min)

**Network Traffic Analysis:**
```spl
index=network sourcetype=firewall
  src_ip="<SUSPECT_SOURCE_IP>"
| stats sum(bytes_out) as total_egress by dest_ip, dest_port
| where total_egress > 100000000
| sort - total_egress
```

**File Access Review:**
```spl
index=wineventlog sourcetype=WinEventLog:Security 
  EventCode IN (4663, 5145)
  Account_Name="<SUSPECT_USER>"
| stats count by Object_Name, Access_Mask
| sort - count
```

---

## 🛡️ Host Isolation Decision Matrix

| Condition | Action | Urgency |
|-----------|--------|---------|
| Critical server accessed (DC, DB) | **Isolate source immediately** | CRITICAL |
| >5 hosts accessed in <10 min | Isolate source, assess targets | HIGH |
| Suspicious processes detected | Isolate affected hosts | HIGH |
| Normal admin activity confirmed | Close alert, document | LOW |
| User verified legitimate activity | Close alert, tune rule | LOW |

---

## 🔒 Containment Actions

### Immediate Actions (Critical)
1. **Disable compromised account** in Active Directory
2. **Isolate source workstation** from network
3. **Block lateral movement** paths (SMB, RDP, WinRM)
4. **Alert identity team** for password reset preparation

### Secondary Actions (High)
1. **Isolate target hosts** if compromise confirmed
2. **Preserve forensic evidence** (memory dumps, disk images)
3. **Review service accounts** with access to affected systems
4. **Check for persistence mechanisms**

---

## 🗺️ Forensic Artifact Collection

### Source Workstation
```
□ Memory dump (volatility analysis)
□ Event logs (Security, System, PowerShell)
□ Browser history and download folder
□ Recent files and jump lists
□ Prefetch files
□ Scheduled tasks and services
```

### Target Hosts
```
□ Security event logs (4624, 4625, 4672, 4688)
□ PowerShell script block logs
□ RDP connection cache
□ SMB session logs
□ Recently created/modified files
□ Registry run keys
```

---

## 📝 Documentation Requirements

| Field | Example |
|-------|---------|
| Alert Time | 2025-12-28 14:35:00 UTC |
| Suspect Account | CORP\admin.service |
| Source IP | 192.168.1.105 |
| Hosts Accessed | WKS001, WKS002, WKS003, SRV-FILE01, SRV-DB01 |
| Movement Duration | 7 minutes |
| Critical Assets | SRV-FILE01, SRV-DB01 |
| User Verified | Yes/No |
| Containment Status | Account disabled, hosts isolated |
| Forensic Preserved | Yes/No |
| Ticket ID | INC-2024-12346 |

---

## ⏱️ SLA Requirements

| Severity | Initial Triage | Investigation | Containment |
|----------|----------------|---------------|-------------|
| High | 10 min | 30 min | 1 hour |
| Critical | 5 min | 15 min | 30 min |

---

## ⚠️ Escalation Triggers

Escalate to **Incident Response Team** if:
- Domain Controller accessed
- Database servers accessed
- Evidence of data exfiltration
- Persistence mechanisms found
- Multiple user accounts compromised
- Attack originated from external IP

---

## 📚 References

- [MITRE ATT&CK T1021](https://attack.mitre.org/techniques/T1021/)
- [Windows Lateral Movement Detection](https://docs.microsoft.com/en-us/advanced-threat-analytics/)
- [SANS Lateral Movement Cheat Sheet](https://www.sans.org/posters/hunt-evil/)
