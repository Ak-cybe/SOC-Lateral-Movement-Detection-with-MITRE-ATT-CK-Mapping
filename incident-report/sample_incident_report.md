# 📋 Security Incident Report

---

## 🏷️ Incident Information

| Field | Value |
|-------|-------|
| **Incident ID** | INC-2024-00472 |
| **Date/Time Detected** | 2025-12-28 14:30:01 UTC |
| **Date/Time Reported** | 2025-12-28 14:35:00 UTC |
| **Incident Handler** | Sarah Chen, SOC Analyst |
| **Status** | Contained |
| **Priority** | **CRITICAL** |

---

## 📝 Executive Summary

A coordinated brute force attack originating from IP address **192.168.1.105** (internal compromised workstation "ATTACKER-PC") successfully compromised the **admin.service** domain service account on December 28, 2024, at 14:31 UTC. Following credential compromise, the attacker rapidly moved laterally across **6 internal systems** within 12 minutes, including critical infrastructure (file server SRV-FILE01 and database server SRV-DB01). 

**Immediate containment actions** were executed: the compromised account was disabled, source workstation isolated, and all target systems are under active monitoring. Forensic investigation is in progress.

---

## 🎯 Incident Classification

| Field | Value |
|-------|-------|
| **Incident Type** | ☑ Brute Force ☑ Credential Compromise ☑ Lateral Movement |
| **Attack Vector** | ☑ Internal (Compromised Workstation) |
| **MITRE ATT&CK Techniques** | T1110, T1078, T1021, T1078.002 |
| **Kill Chain Stage** | ☑ Initial Access ☑ Lateral Movement ☑ Privilege Escalation |

---

## 🔍 Technical Details

### Threat Actor Information

| Field | Value |
|-------|-------|
| **Source IP** | 192.168.1.105 |
| **Source Hostname** | ATTACKER-PC |
| **Geographic Location** | Internal Network (Building A, Floor 3) |
| **IP Reputation** | N/A (Internal) |
| **Known Threat Actor** | ☐ Yes ☑ No ☐ Unknown |

### Compromised Assets

| Asset | Type | Criticality | Access Level |
|-------|------|-------------|--------------|
| DC01.corp.local | Domain Controller | CRITICAL | Admin |
| WKS001.corp.local | Workstation | LOW | User |
| WKS002.corp.local | Workstation | LOW | User |
| WKS003.corp.local | Workstation | LOW | User |
| SRV-FILE01.corp.local | File Server | HIGH | Admin |
| SRV-DB01.corp.local | Database Server | CRITICAL | Admin |

### Compromised Accounts

| Account | Domain | Privilege Level | Status |
|---------|--------|-----------------|--------|
| admin.service | CORP | Domain Admin | **DISABLED** |

### Attack Timeline

| Time (UTC) | Event | EventCode | Target | Details |
|------------|-------|-----------|--------|---------|
| 14:30:01 | Brute Force Start | 4625 | DC01 | First failed login attempt |
| 14:30:54 | Brute Force End | 4625 | DC01 | 20th failed login attempt |
| 14:31:05 | **Credential Compromise** | 4624 | DC01 | Successful login after brute force |
| 14:31:06 | Privilege Abuse | 4672 | DC01 | High privileges assigned |
| 14:35:12 | Lateral Movement | 4624 | WKS001 | First lateral authentication |
| 14:36:45 | Lateral Movement | 4624 | WKS002 | Second host accessed |
| 14:38:22 | Lateral Movement | 4624 | WKS003 | Third host accessed |
| 14:40:55 | **Critical Asset Access** | 4624 | SRV-FILE01 | File server compromised |
| 14:42:30 | **Critical Asset Access** | 4624 | SRV-DB01 | Database server compromised |
| 14:42:31 | Privilege Abuse | 4672 | SRV-DB01 | Admin privileges on DB server |

**Total Attack Duration**: 12 minutes 30 seconds

---

## 📊 Impact Assessment

### Business Impact

| Category | Impact Level | Description |
|----------|--------------|-------------|
| Data Confidentiality | **HIGH** | Access to file and database servers |
| Data Integrity | **MEDIUM** | No evidence of modification (under investigation) |
| System Availability | **LOW** | No service disruption during attack |
| Financial Impact | $50,000 - $150,000 estimated | Investigation, remediation, potential disclosure |
| Regulatory/Compliance | **Pending** | GDPR/PCI-DSS review required |
| Reputation Risk | **MEDIUM** | Internal incident, no customer data confirmed |

### Data at Risk

| Data Type | Volume | Classification | Exfiltrated |
|-----------|--------|----------------|-------------|
| Employee PII | ~5,000 records | Confidential | ☐ Yes ☐ No ☑ Unknown |
| Financial Data | Unknown | Restricted | ☐ Yes ☐ No ☑ Unknown |
| Customer Database | Unknown | Confidential | ☐ Yes ☐ No ☑ Unknown |

---

## 🛡️ Response Actions

### Containment

| Action | Status | Timestamp | Performed By |
|--------|--------|-----------|--------------|
| Account disabled | ☑ Done | 14:45:00 | Sarah Chen |
| Source IP blocked | ☑ Done | 14:47:00 | Network Team |
| Host(s) isolated | ☑ Done | 14:50:00 | Endpoint Team |
| Password reset initiated | ☐ Pending | - | Identity Team |

### Eradication

| Action | Status | Timestamp | Performed By |
|--------|--------|-----------|--------------|
| Malware scan on source | ☐ In Progress | - | IR Team |
| Persistence check | ☐ In Progress | - | IR Team |
| Vulnerabilities patched | ☐ Pending | - | IT Operations |
| Credentials rotated | ☐ Pending | - | Identity Team |

### Recovery

| Action | Status | Timestamp | Performed By |
|--------|--------|-----------|--------------|
| Systems restored | ☐ Pending | - | IT Operations |
| Monitoring enhanced | ☑ Done | 15:00:00 | SOC Team |
| Verification testing | ☐ Pending | - | QA Team |
| Return to production | ☐ Pending | - | IT Operations |

---

## 🔬 Root Cause Analysis

### Primary Cause
The **admin.service** account was configured with a weak password that was susceptible to brute force attack. The account lacked multi-factor authentication (MFA) protection.

### Contributing Factors
- ☑ Weak credentials (password in top 1000 common passwords)
- ☑ Missing MFA for service accounts
- ☐ Insufficient monitoring (detection worked as expected)
- ☐ Misconfiguration
- ☐ Unpatched vulnerability
- ☐ Social engineering
- ☐ Other

### Detection Gap Analysis
| What Worked | What Failed | Improvement Needed |
|-------------|-------------|-------------------|
| Brute force detection triggered at 14:30 | No automated response | Implement SOAR playbook for auto-disable after threshold |
| Kill chain alert correlated all stages | 10-minute detection delay | Reduce correlation window |
| SOC analyst responded within 15 min | No account lockout triggered | Enforce account lockout policy |

---

## 📚 Evidence Collected

| Evidence Type | Location | Hash (SHA256) | Collected By | Date |
|---------------|----------|---------------|--------------|------|
| Memory Dump | \\forensics\INC-2024-00472\ATTACKER-PC.mem | 3a7f8c9d... | IR Team | 2025-12-28 |
| Event Logs (DC01) | \\forensics\INC-2024-00472\DC01_Security.evtx | b2e5f4a1... | SOC Team | 2025-12-28 |
| Event Logs (SRV-DB01) | \\forensics\INC-2024-00472\SRV-DB01_Security.evtx | c8d2e1b3... | SOC Team | 2025-12-28 |
| Network Capture | \\forensics\INC-2024-00472\traffic.pcap | 9f1a2b3c... | Network Team | 2025-12-28 |

---

## ✅ Recommendations

### Immediate (0-7 days)
1. **Enforce MFA** for all admin and service accounts
2. **Rotate all credentials** for admin.service and any related accounts
3. **Full forensic analysis** of SRV-FILE01 and SRV-DB01 for data exfiltration
4. **Implement account lockout policy**: 5 failed attempts = 30-minute lockout

### Short-term (7-30 days)
1. **Deploy SOAR playbook** for automated account disable on brute force + success
2. **Review all service account passwords** against breach databases
3. **Implement Privileged Access Workstations (PAW)** for admin activities
4. **Conduct user security awareness training** on compromised workstation owner

### Long-term (30+ days)
1. **Implement Zero Trust architecture** for critical server access
2. **Deploy EDR solution** for enhanced process visibility
3. **Quarterly password audits** for all privileged accounts
4. **Red team exercise** to validate detection improvements

---

## 📋 Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| SOC Analyst | Sarah Chen | _________ | 2025-12-28 |
| SOC Manager | Michael Rodriguez | _________ | 2025-12-28 |
| CISO | Jennifer Walsh | _________ | 2025-12-28 |

---

## 📝 Lessons Learned

*To be completed during post-incident review (scheduled: 2025-12-30)*

| Question | Response |
|----------|----------|
| What went well? | Kill chain detection worked, alert correlation was accurate |
| What could be improved? | Faster automated response, account lockout policy |
| What actions will prevent recurrence? | MFA enforcement, SOAR automation |
| Were playbooks adequate? | Yes, brute force playbook followed correctly |
| Were tools effective? | Splunk correlation effective, need SOAR integration |

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-28  
**Classification**: CONFIDENTIAL
