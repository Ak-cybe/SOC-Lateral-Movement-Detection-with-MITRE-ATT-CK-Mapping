# 🛣️ Project Roadmap

This document tracking the prioritized engineering tasks for the SOC Lateral Movement Detection project.

## 🔴 P0 - Critical for Deployment (This Week)
*Must be completed before initial production deployment.*

| Item | Acceptance Criteria | Effort | Status |
|------|---------------------|--------|--------|
| **Add lookup files** | `admin_jump_servers.csv`, `service_accounts.csv` present in `lookups/` | 2h | ✅ Done |
| **Fix Splunk Kill Chain Rule** | `kill_chain_alert.spl` uses `eventstats` (no nested joins), <3min latency | 4h | ✅ Done |
| **Telemetry Configs** | `sysmon_config.xml` & `windows_audit_policy.xml` in `configs/` | 3h | ✅ Done |
| **Validation Script** | `scripts/replay_attack_scenario.py` ingests logs & generates expected alerts | 6h | ✅ Done |
| **Severity Scoring Matrix** | `docs/severity_matrix.md` defines clear calculation formulas | 2h | ✅ Done |

**Total P0 Effort:** ~17 hours

---

## 🟡 P1 - Operational Excellence (Next Sprint)
*Focus on improving analyst workflow and accuracy.*

| Item | Acceptance Criteria | Effort | Status |
|------|---------------------|--------|--------|
| **Correct MITRE T1078.002** | Remove 4672-only mapping, enforce context requirements | 2h | ✅ Done |
| **Add Password Spray Rule** | New Splunk/Elastic detection for T1110.003 | 4h | ✅ Done |
| **Architecture Diagram** | `docs/architecture.md` with dataflow visualization | 3h | ✅ Done |
| **SOAR Integration** | Webhook action added to Elastic rules | 3h | ✅ Done |
| **Troubleshooting Guide** | `docs/troubleshooting.md` with solutions for common issues | 4h | ✅ Done |
| **Baseline Data Script** | Script to analyze 7-day logs for normaladmin patterns | 6h | 📝 Todo |

**Total P1 Effort:** ~22 hours

---

## 🟢 P2 - Enhancements (Nice-to-Have)
*Advanced features for mature SOCs.*

| Item | Acceptance Criteria | Effort | Status |
|------|---------------------|--------|--------|
| **Sigma Rule Conversion** | Convert SPL rules to Sigma for portability | 8h | 📝 Todo |
| **Jupyter Analysis NB** | Interactive notebook for Tier-3 analysts | 6h | 📝 Todo |
| **GeoIP Enforcement** | Auto-block auth from anomalous countries (Firewall integration) | 4h | 📝 Todo |
| **Threat Intel Feeds** | Auto-check attacker IPs against AbuseIPDB/AlienVault | 8h | 📝 Todo |
| **Grafana Dashboard** | Visualize Alert Volume, FP Rate, MTTR | 10h | 📝 Todo |

**Total P2 Effort:** ~36 hours
