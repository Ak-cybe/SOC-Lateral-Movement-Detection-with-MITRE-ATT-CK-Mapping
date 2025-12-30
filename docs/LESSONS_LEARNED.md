# 🎓 Lessons Learned for Detection Engineers

> "Documentation ≠ Detection"

This document captures key takeaways from the development and operationalization of this detection suite.

## 1. Documentation ≠ Detection
A fancy `README.md` with animated headers and screenshots implies maturity, but does not guarantee production readiness. True maturity lies in:
-   **Unit Tests:** Does the SPL/KQL syntax actually work?
-   **Validation Scripts:** Can you replay an attack and trigger the rule?
-   **Config Files:** Are the GPO and Sysmon requirements documented explicitly?

## 2. Context Matters for MITRE Mapping
Mapping Event ID **4672** (Special Privileges Assigned) directly to **Privilege Escalation** (T1068) is a common mistake.
-   **Reality:** 4672 happens on *every* legitimate admin logon.
-   **Fix:** It requires context (Time of Day, Source IP, previous 4625s) to be a T1078.002 indicator.

## 3. False Positives Kill Trust
If a rule alerts on every administrative login (e.g., Jump Server activity), analysts will ignore it ("Alert Fatigue").
-   **Requirement:** Day-1 inclusion of generic `lookups/` (allowlists) is mandatory.
-   **Requirement:** Rules must have `NOT [ inputlookup ... ]` filters logic built-in.

## 4. Validation is Mandatory
"It works on my machine" is not acceptable security engineering.
-   If you don't have a `scripts/ingest_logs.py` or `tests/expected_alerts.json`, your detection is theoretical.
-   Always provide a way to verify the "Green" state.

## 5. Operationalize Early
Finding an attack is only 10% of the job.
-   **SOAR Integration:** Plan for how the alert leaves the SIEM.
-   **Playbooks:** Detection rules should reference specific steps in a playbook (e.g., "See Step 3 for IP Reputation").
-   **Severity:** Define math-based severity early to avoid subjective prioritization.
