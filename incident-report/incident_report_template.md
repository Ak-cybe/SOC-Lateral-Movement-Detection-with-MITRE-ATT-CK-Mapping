# 📋 Security Incident Report Template

---

## 🏷️ Incident Information

| Field | Value |
|-------|-------|
| **Incident ID** | INC-YYYY-XXXXX |
| **Date/Time Detected** | YYYY-MM-DD HH:MM:SS UTC |
| **Date/Time Reported** | YYYY-MM-DD HH:MM:SS UTC |
| **Incident Handler** | [Name] |
| **Status** | Open / Investigating / Contained / Eradicated / Closed |
| **Priority** | Critical / High / Medium / Low |

---

## 📝 Executive Summary

[Provide a 2-3 sentence summary of the incident for management. Include what happened, impact, and current status.]

**Example**:
> A brute force attack originating from external IP X.X.X.X successfully compromised the admin.service account on December 28, 2024. The attacker subsequently moved laterally to 5 internal systems including file and database servers. The account has been disabled and affected systems are isolated pending forensic analysis.

---

## 🎯 Incident Classification

| Field | Value |
|-------|-------|
| **Incident Type** | □ Brute Force □ Credential Compromise □ Lateral Movement □ Data Exfiltration □ Malware □ Other |
| **Attack Vector** | □ External □ Internal □ Unknown |
| **MITRE ATT&CK Techniques** | T1110, T1078, T1021, T1078.002 |
| **Kill Chain Stage** | □ Reconnaissance □ Initial Access □ Execution □ Persistence □ Privilege Escalation □ Lateral Movement □ Collection □ Exfiltration |

---

## 🔍 Technical Details

### Threat Actor Information

| Field | Value |
|-------|-------|
| **Source IP(s)** | |
| **Source Hostname(s)** | |
| **Geographic Location** | |
| **IP Reputation** | |
| **Known Threat Actor** | □ Yes □ No □ Unknown |

### Compromised Assets

| Asset | Type | Criticality | Access Level |
|-------|------|-------------|--------------|
| | | | |
| | | | |
| | | | |

### Compromised Accounts

| Account | Domain | Privilege Level | Status |
|---------|--------|-----------------|--------|
| | | | |
| | | | |

### Attack Timeline

| Time (UTC) | Event | Source | Target | Details |
|------------|-------|--------|--------|---------|
| | | | | |
| | | | | |
| | | | | |

---

## 📊 Impact Assessment

### Business Impact

| Category | Impact Level | Description |
|----------|--------------|-------------|
| Data Confidentiality | None / Low / Medium / High / Critical | |
| Data Integrity | None / Low / Medium / High / Critical | |
| System Availability | None / Low / Medium / High / Critical | |
| Financial Impact | $X estimated | |
| Regulatory/Compliance | Yes / No / Pending | |
| Reputation Risk | Low / Medium / High | |

### Data at Risk

| Data Type | Volume | Classification | Exfiltrated |
|-----------|--------|----------------|-------------|
| | | | □ Yes □ No □ Unknown |
| | | | □ Yes □ No □ Unknown |

---

## 🛡️ Response Actions

### Containment

| Action | Status | Timestamp | Performed By |
|--------|--------|-----------|--------------|
| Account disabled | □ Done □ Pending | | |
| Source IP blocked | □ Done □ Pending | | |
| Host(s) isolated | □ Done □ Pending | | |
| Password reset initiated | □ Done □ Pending | | |

### Eradication

| Action | Status | Timestamp | Performed By |
|--------|--------|-----------|--------------|
| Malware removed | □ Done □ N/A | | |
| Persistence mechanisms removed | □ Done □ N/A | | |
| Vulnerabilities patched | □ Done □ N/A | | |
| Credentials rotated | □ Done □ Pending | | |

### Recovery

| Action | Status | Timestamp | Performed By |
|--------|--------|-----------|--------------|
| Systems restored | □ Done □ Pending | | |
| Monitoring enhanced | □ Done □ Pending | | |
| Verification testing | □ Done □ Pending | | |
| Return to production | □ Done □ Pending | | |

---

## 🔬 Root Cause Analysis

### Primary Cause
[Describe the primary cause of the incident]

### Contributing Factors
- [ ] Weak credentials
- [ ] Missing MFA
- [ ] Insufficient monitoring
- [ ] Misconfiguration
- [ ] Unpatched vulnerability
- [ ] Social engineering
- [ ] Other: ___________

### Detection Gap Analysis
| What Worked | What Failed | Improvement Needed |
|-------------|-------------|-------------------|
| | | |
| | | |

---

## 📚 Evidence Collected

| Evidence Type | Location | Hash (SHA256) | Collected By | Date |
|---------------|----------|---------------|--------------|------|
| Memory Dump | | | | |
| Disk Image | | | | |
| Event Logs | | | | |
| Network Captures | | | | |
| Screenshots | | | | |

---

## ✅ Recommendations

### Immediate (0-7 days)
1. 
2. 
3. 

### Short-term (7-30 days)
1. 
2. 
3. 

### Long-term (30+ days)
1. 
2. 
3. 

---

## 📎 Attachments

- [ ] Alert screenshots
- [ ] Timeline diagram
- [ ] Network diagrams
- [ ] IOC list
- [ ] Forensic report

---

## 📋 Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| SOC Analyst | | | |
| SOC Manager | | | |
| CISO (if Critical) | | | |

---

## 📝 Lessons Learned

[To be completed during post-incident review meeting]

| Question | Response |
|----------|----------|
| What went well? | |
| What could be improved? | |
| What actions will prevent recurrence? | |
| Were playbooks adequate? | |
| Were tools effective? | |

---

**Document Version**: 1.0  
**Last Updated**: YYYY-MM-DD  
**Classification**: CONFIDENTIAL
