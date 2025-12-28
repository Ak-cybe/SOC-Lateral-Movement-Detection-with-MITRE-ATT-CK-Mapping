# ⚠️ False Positive Handling Guide

## Overview

This document outlines known false positive sources for the lateral movement detection rules and provides tuning recommendations for production deployment.

---

## 🏢 Common False Positive Sources

### 1. IT Administrator Activity

**Pattern**: IT staff legitimately accessing multiple hosts for maintenance

**Indicators**:
- Source IP is from IT subnet or jump server
- Activity during business hours or scheduled maintenance
- User is member of IT/Admin groups
- Access pattern matches change tickets

**Tuning**:
```spl
| search NOT [| inputlookup admin_jump_servers.csv | fields Source_Network_Address]
| search NOT [| inputlookup it_admin_accounts.csv | fields Account_Name]
```

**Exclusion List Template** (`admin_jump_servers.csv`):
```csv
Source_Network_Address,Description
10.0.1.100,IT Jump Server 1
10.0.1.101,IT Jump Server 2
10.0.1.102,Help Desk Jump Server
```

---

### 2. Service Accounts

**Pattern**: Automated systems accessing multiple hosts

**Indicators**:
- Account name ends with `$` (computer account)
- Account name contains `svc`, `service`, `auto`
- Regular, predictable access pattern
- No interactive logon type

**Tuning**:
```spl
| where NOT match(Account_Name, "(?i)(svc|service|\$|automation|backup)")
```

**Exclusion List Template** (`service_accounts.csv`):
```csv
Account_Name,Description,Owner
svc.backup,Backup Service,IT Operations
svc.monitoring,Monitoring Agent,NOC
svc.patching,WSUS Update Agent,IT Operations
SCCM$,SCCM Client,IT Operations
```

---

### 3. Patch Deployment & Updates

**Pattern**: WSUS/SCCM pushing updates to multiple hosts

**Indicators**:
- Activity during patch window (e.g., Tuesdays, maintenance windows)
- Source is WSUS/SCCM server
- Identical access times across many hosts

**Tuning**:
```spl
| eval is_patch_window = if(
    date_wday="tuesday" AND date_hour >= 22 AND date_hour <= 6, 
    1, 0)
| where is_patch_window = 0 OR match(Account_Name, "(?i)sccm|wsus")
```

**Maintenance Window Template** (`maintenance_windows.csv`):
```csv
window_name,start_time,end_time,days
Patch_Tuesday,22:00,06:00,tuesday
Monthly_Maintenance,01:00,05:00,first_saturday
```

---

### 4. Monitoring & Inventory Tools

**Pattern**: Nagios, Zabbix, SCOM, or similar tools polling hosts

**Indicators**:
- Source is monitoring server IP
- Consistent interval between accesses
- Read-only access patterns
- Account is monitoring service account

**Tuning**:
```spl
| search NOT [| inputlookup monitoring_servers.csv | fields Source_Network_Address]
```

---

### 5. Help Desk Remote Support

**Pattern**: Help desk accessing user workstations for support

**Indicators**:
- Source is from help desk subnet
- RDP logon type (10)
- Coincides with support tickets
- Short session duration

**Recommendation**: 
- Cross-reference with ticketing system
- Implement time-based correlation with ticket creation

---

## 📊 Baseline Thresholds

| Parameter | Default | Recommended Tuning Range |
|-----------|---------|--------------------------|
| Distinct hosts threshold | ≥3 | 3-5 (adjust based on baseline) |
| Time window | 10 min | 10-30 min |
| Failed login threshold | >5 | 5-10 |
| Brute force window | 5 min | 3-5 min |

---

## 🔧 Tuning Process

### Step 1: Baseline Analysis (Week 1-2)
```spl
index=wineventlog sourcetype=WinEventLog:Security EventCode=4624
| stats dc(ComputerName) as hosts_per_day by Account_Name, date_mday
| stats avg(hosts_per_day) as avg_hosts max(hosts_per_day) as max_hosts by Account_Name
| where avg_hosts > 3
| sort - avg_hosts
```

### Step 2: Identify Normal Patterns
- Document peak access times
- Identify high-activity accounts
- Map IT/admin access patterns

### Step 3: Create Exclusion Lists
- Admin jump servers
- Service accounts
- Monitoring systems
- Maintenance windows

### Step 4: Threshold Adjustment
- Start with conservative thresholds
- Monitor false positive rate
- Adjust threshold incrementally (1 host at a time)

### Step 5: Continuous Tuning
- Review weekly FP metrics
- Update exclusion lists as infrastructure changes
- Re-baseline quarterly

---

## 📈 False Positive Metrics

Track these metrics weekly:

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| FP Rate | <10% | Review exclusion lists |
| FP per Week | <20 | Increase thresholds |
| FP per Rule | <5 each | Per-rule tuning |
| Analyst Time on FPs | <2 hrs/week | Automate checks |

---

## 🚨 Do NOT Exclude

**Never add to exclusion lists**:
- External IPs
- Newly created accounts
- Recently modified service accounts
- Accounts with recent password changes
- Accounts from terminated employees

---

## 📝 Change Control

Any modification to exclusion lists or thresholds must:
1. Be documented with justification
2. Be approved by SOC Lead
3. Include rollback plan
4. Be reviewed after 30 days
