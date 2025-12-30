# 📋 Detection Improvement Checklist

Use this checklist to track the maturity and operational readiness of the SOC Lateral Movement Detection project.

## 🪵 Logging Prerequisites
- [x] **Windows Audit Policy configured** (Logon/Logoff events enabled) -> *See `configs/windows_audit_policy.xml`*
- [x] **Sysmon deployed** (Process, Network events specific to lateral movement) -> *See `configs/sysmon_config.xml`*
- [ ] **Event forwarding to SIEM validated** (Check `docs/log_forwarding_guide.md`)
- [ ] **Required fields present** (`Source_Network_Address`, `Account_Name`, `ComputerName`)
- [ ] **Log retention** (90 days minimum recommended)

## 💡 Correlation Ideas (Future Roadmap)
- [x] **Brute Force + GeoIP anomaly** (Added to Elastic rule)
- [ ] **Brute Force + Failed MFA attempts** (Requires Azure AD integration)
- [ ] **Lateral Movement + Data exfiltration** (Requires Firewall/Proxy logs)
- [x] **Privilege Abuse + Suspicious process execution** (Covered by Sysmon logic)
- [ ] **Threat Intel Feed** (Check attacker IP against known bad actors)

## 🛠️ FP Tuning Notes
- [x] **Create exclusion lists** (Done: `lookups/admin_jump_servers.csv`, `service_accounts.csv`)
- [ ] **Baseline normal admin activity** (Collect 1 week of data before enabling block actions)
- [ ] **Implement time-of-day filters** (Avoid alerting during patch windows)
- [x] **Add user role context** (Severity Matrix accounts for Admin vs User)
- [ ] **Weekly FP review meeting** (Tune thresholds based on `distinct_hosts` metrics)

## ✅ Validation Approach
- [x] **Unit testing** (Validate regex/SPL syntax)
- [x] **Integration testing** (Use `scripts/replay_attack_scenario.py`)
- [x] **Expected behavior defined** (See `tests/expected_alerts.json`)
- [ ] **Baseline testing** (7-day silent run to measure FP rate)
- [ ] **Acceptance criteria** (FP rate <10%, detection latency <5min)
