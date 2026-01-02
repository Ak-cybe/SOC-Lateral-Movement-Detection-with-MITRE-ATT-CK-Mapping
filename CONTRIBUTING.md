# Contributing to SOC Lateral Movement Detection

Thank you for your interest in contributing to this project! This document provides guidelines and best practices for contributing detection rules, playbooks, and documentation.

## 🤝 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs, false positives, or detection gaps
- Include the following in your report:
  - Rule name and file path
  - Expected behavior vs actual behavior
  - Sample logs (sanitized/anonymized) if possible
  - Environment details (Splunk/Elastic version)

### Proposing New Detections
Before creating a new detection rule:
1. Check if the technique is already covered in `investigation-playbook/mitre_attack_mapping.md`
2. Ensure you have realistic test data to validate the detection
3. Consider false positive sources and document tuning recommendations

### Pull Request Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-detection-t1xxx`
3. Make your changes following the standards below
4. Test your changes using `scripts/replay_attack_scenario.py`
5. Submit a PR with a clear description

## 📋 Detection Rule Standards

### Splunk SPL Rules
- Use triple backticks for comments (not single backticks which are macro syntax)
- Always include `sourcetype=` for performance
- Include MITRE ATT&CK technique IDs in header comments
- Add tuning knobs (thresholds as variables where possible)

**Template:**
```spl
``` Detection Name
    Purpose: What does this detect?
    MITRE ATT&CK: T1XXX, T1XXX.XXX
    Data Sources: WinEventLog:Security, etc.
    Author: Your Name
    Version: 1.0
```

index=wineventlog sourcetype=WinEventLog:Security EventCode=XXXX
| ... your logic ...
| eval severity = case(...)
| table _time, Account_Name, severity, mitre_technique
```

### Elastic Security Rules
- Follow the [Elastic Detection Rule Schema](https://www.elastic.co/guide/en/security/current/rules-api-create.html)
- Include `threat` array with proper MITRE mapping
- Add `investigation_guide` for analyst context
- Document `false_positives` and `required_fields`

## 📁 Directory Structure

| Directory | Purpose |
|-----------|---------|
| `correlation-rules/splunk/` | SPL detection rules |
| `correlation-rules/elastic/` | Elastic JSON detection rules |
| `investigation-playbook/` | Analyst response playbooks |
| `configs/` | Telemetry configuration files |
| `lookups/` | Exclusion lists (CSV format) |
| `logs/` | Sample log data for testing |
| `tests/` | Expected alert outputs |
| `docs/` | Architecture and operational documentation |

## ✅ Checklist Before Submitting

- [ ] Detection includes MITRE ATT&CK mapping
- [ ] False positive sources are documented
- [ ] Required log fields/sources are specified
- [ ] Tuning recommendations are provided
- [ ] Test data in `logs/` updated if needed
- [ ] Expected alerts in `tests/expected_alerts.json` updated
- [ ] README updated if adding new capabilities

## 🧪 Testing Your Changes

1. Deploy rules to your test SIEM environment
2. Run the replay script:
   ```bash
   python scripts/replay_attack_scenario.py
   ```
3. Verify alerts match `tests/expected_alerts.json`
4. Document any new false positive patterns

## 📝 Commit Message Format

Use conventional commits:
- `feat: add T1110.002 password cracking detection`
- `fix: correct field mapping in lateral movement rule`
- `docs: update playbook with new pivot queries`
- `test: add validation data for password spraying`

## 📜 Code of Conduct

- Be respectful and constructive in all interactions
- Focus on improving detection capabilities
- Share knowledge and help others learn
- Report security issues responsibly

## 🔒 Security

If you discover a security vulnerability in the detection logic that could lead to bypass, please report it privately to the maintainers rather than opening a public issue.

---

**Questions?** Open an issue or reach out to the maintainers.

Thank you for helping make this project better! 🛡️
