# 🔧 Detection Engineering Notes

This document provides practical guidance for tuning, maintaining, and extending the lateral movement detection capabilities.

---

## 📊 False Positive Tuning Workflow

### Phase 1: Initial Deployment (Week 1)
1. Deploy rules in **alert-only mode** (no automated response)
2. Set thresholds conservatively high:
   - Brute Force: >10 attempts (instead of 5)
   - Lateral Movement: ≥5 hosts (instead of 3)
3. Review 100% of alerts manually

### Phase 2: Baseline Collection (Week 2-3)
Run this query daily to establish normal patterns:
```spl
index=wineventlog EventCode=4624 earliest=-7d
| stats dc(ComputerName) as daily_hosts by Account_Name, date_mday
| stats avg(daily_hosts) as avg, max(daily_hosts) as max, stdev(daily_hosts) as stddev by Account_Name
| where avg > 2
| sort - max
```

Use output to:
- Identify high-activity accounts (candidates for exclusion or higher thresholds)
- Establish per-user baseline thresholds
- Document IT maintenance patterns

### Phase 3: Threshold Optimization (Week 4+)
Adjust thresholds based on:
- **FP Rate Target**: <10% of alerts should be false positives
- **Detection Latency**: Alerts should fire within 15 minutes of activity start
- **Coverage**: Ensure at least 90% of known-bad patterns trigger alerts

---

## 📈 Key Performance Metrics

Track these metrics weekly:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **True Positive Rate** | >90% | (Confirmed attacks / Total alerts) |
| **False Positive Rate** | <10% | (FPs / Total alerts) |
| **Mean Time to Detect** | <15 min | Alert time - First malicious event time |
| **Mean Time to Triage** | <30 min | Analyst investigation start - Alert time |
| **Coverage** | 100% of T1021/T1110 | Manual red team validation |

---

## 🔍 Data Quality Checks

Run these checks weekly to ensure detection reliability:

### 1. Field Completeness Check
```spl
index=wineventlog EventCode=4625 earliest=-1d
| eval ip_present = if(isnotnull(Source_Network_Address) AND Source_Network_Address!="-", 1, 0)
| stats count as total, sum(ip_present) as has_ip
| eval completeness = round(has_ip/total*100, 1)
| table total, has_ip, completeness
```
**Target**: >95% completeness for Source_Network_Address

### 2. Time Sync Check
```spl
index=wineventlog EventCode=4624 earliest=-1h
| eval time_diff = abs(_time - now())
| stats max(time_diff) as max_drift_seconds
| eval status = if(max_drift_seconds > 300, "CRITICAL: Time sync issue", "OK")
| table max_drift_seconds, status
```
**Target**: Max drift <5 minutes

### 3. Volume Anomaly Detection
```spl
index=wineventlog EventCode=4625 earliest=-7d
| bucket _time span=1h
| stats count by _time
| eventstats avg(count) as baseline, stdev(count) as stddev
| eval zscore = (count - baseline) / stddev
| where abs(zscore) > 3
| table _time, count, zscore
```
**Action**: Investigate hours with z-score >3 (potential attack or data quality issue)

---

## 🔄 Maintenance Checklist

### Monthly Tasks
- [ ] Review and update exclusion lists (`lookups/*.csv`)
- [ ] Audit service accounts for changes
- [ ] Review alert volume trends
- [ ] Update MITRE ATT&CK mappings for new techniques

### Quarterly Tasks
- [ ] Conduct red team validation (test detection coverage)
- [ ] Review detection gap analysis
- [ ] Update severity scoring based on environment changes
- [ ] Archive and analyze closed incidents for pattern updates

### Annual Tasks
- [ ] Full detection logic review and optimization
- [ ] Update Sysmon and audit policy configurations
- [ ] Conduct tabletop exercise with incident reports
- [ ] Document lessons learned and update playbooks

---

## 🛡️ Common Exclusion Patterns

### Service Account Patterns
```csv
# Add to lookups/service_accounts.csv
account_name,type,description
svc.*,service,Standard service account naming
*-svc,service,Alternate service account naming
*_automation,service,Automation accounts
scanner.*,scanner,Security scanners
backup.*,backup,Backup service accounts
```

### Jump Server IP Ranges
```csv
# Add to lookups/admin_jump_servers.csv
ip,hostname,description
10.0.1.0/24,,IT Admin Subnet
10.0.2.0/24,,Security Operations Subnet
172.16.100.0/24,,PAW Workstations
```

---

## ⚠️ Known Limitations

1. **Local Account Logins**: 4624/4625 may not capture source IP for local console logins
2. **Kerberos Authentication**: Some network logins may show DC IP instead of actual source
3. **Cloud-Federated Accounts**: Azure AD joined devices may have different event patterns
4. **VPN Split Tunneling**: Source IP may show internal VPN concentrator, not actual client

---

## 📚 Recommended Reading

- [MITRE ATT&CK Lateral Movement](https://attack.mitre.org/tactics/TA0008/)
- [Splunk Security Essentials](https://splunkbase.splunk.com/app/3435/)
- [Elastic Detection Engineering Guide](https://www.elastic.co/guide/en/security/current/rules-api-overview.html)
- [Windows Security Event Reference](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/security-auditing-overview)

---

**Last Updated**: January 2025  
**Maintainer**: SOC Detection Engineering Team
