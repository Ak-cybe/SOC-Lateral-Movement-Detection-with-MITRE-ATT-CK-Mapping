# 🛠️ Hands-On Practice Guide: SOC Lateral Movement Detection Lab

## 🖥️ Your Lab Setup

| System | Role | IP (Example) |
|--------|------|--------------|
| **Kali Linux** | Attacker Machine | 192.168.1.100 |
| **Windows Server 2019** | Target/Victim | 192.168.1.10 |
| **Splunk** | SIEM (can run on either) | 192.168.1.50:8000 |

---

## 📋 Prerequisites Checklist

```
□ Kali Linux running
□ Windows Server 2019 running  
□ Both machines on same network (can ping each other)
□ Splunk installed and accessible
□ Windows account created for testing (e.g., "testuser")
```

---

# PHASE 1: Windows Server 2019 Configuration

## Step 1.1: Enable Security Auditing

**Open PowerShell as Administrator on Windows Server 2019:**

```powershell
# Enable Audit Logon Events (Success + Failure)
auditpol /set /subcategory:"Logon" /success:enable /failure:enable

# Enable Special Logon auditing
auditpol /set /subcategory:"Special Logon" /success:enable

# Verify audit settings
auditpol /get /category:"Logon/Logoff"
```

**Expected Output:**
```
Logon                               Success and Failure
Special Logon                       Success
```

## Step 1.2: Create Test User Account

```powershell
# Create a user for brute force practice
net user testuser Password123! /add

# Add to Administrators group (for privilege testing)
net localgroup Administrators testuser /add

# Verify user created
net user testuser
```

## Step 1.3: Enable Remote Desktop (RDP)

```powershell
# Enable RDP
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0

# Allow RDP through firewall
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"

# Check RDP status
Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections"
```

## Step 1.4: Enable SMB (for lateral movement simulation)

```powershell
# SMB is enabled by default, verify it
Get-SmbServerConfiguration | Select EnableSMB2Protocol

# Open firewall for SMB
Enable-NetFirewallRule -DisplayGroup "File and Printer Sharing"
```

---

# PHASE 2: Splunk Configuration

## Step 2.1: Install Splunk Universal Forwarder on Windows Server

**Download and Install:**
```powershell
# Download Splunk Universal Forwarder (run in browser or wget)
# https://www.splunk.com/en_us/download/universal-forwarder.html

# After installation, configure inputs
cd "C:\Program Files\SplunkUniversalForwarder\bin"

# Add Windows Security logs
.\splunk add monitor "C:\Windows\System32\winevt\Logs\Security.evtx" -sourcetype WinEventLog:Security
```

## Step 2.2: Configure inputs.conf (Alternative Method)

**Create/Edit: `C:\Program Files\SplunkUniversalForwarder\etc\system\local\inputs.conf`**

```ini
[WinEventLog://Security]
disabled = 0
start_from = oldest
current_only = 0
evt_resolve_ad_obj = 1
checkpointInterval = 5
```

## Step 2.3: Configure outputs.conf

**Create/Edit: `C:\Program Files\SplunkUniversalForwarder\etc\system\local\outputs.conf`**

```ini
[tcpout]
defaultGroup = splunk_indexer

[tcpout:splunk_indexer]
server = 192.168.1.50:9997
```

## Step 2.4: Restart Splunk Forwarder

```powershell
cd "C:\Program Files\SplunkUniversalForwarder\bin"
.\splunk restart
```

## Step 2.5: Verify Data in Splunk Web

**Open Splunk Web (http://192.168.1.50:8000):**

```spl
# Search for Windows Security logs
index=main sourcetype=WinEventLog:Security
| head 10
```

---

# PHASE 3: Generate Attack Traffic from Kali

## Step 3.1: Brute Force Attack with Hydra

**On Kali Linux Terminal:**

```bash
# Test connectivity first
ping 192.168.1.10

# Create password wordlist
echo -e "password\n123456\nwrongpass\nbadpass\ntest123\nPassword123!" > passwords.txt

# Create username list
echo -e "testuser\nadmin\nadministrator" > users.txt

# Brute Force RDP (Port 3389)
hydra -L users.txt -P passwords.txt rdp://192.168.1.10 -t 4 -V

# Brute Force SMB (Port 445)
hydra -L users.txt -P passwords.txt smb://192.168.1.10 -t 4 -V
```

## Step 3.2: Brute Force with Ncrack

```bash
# Alternative tool for RDP brute force
ncrack -u testuser -P passwords.txt 192.168.1.10:3389 -v
```

## Step 3.3: Brute Force with CrackMapExec (Recommended)

```bash
# Install if not present
sudo apt install crackmapexec -y

# SMB Brute Force
crackmapexec smb 192.168.1.10 -u testuser -p passwords.txt

# This will generate Event ID 4625 on Windows Server
```

## Step 3.4: Successful Login After Brute Force

```bash
# After brute force, login with correct credentials
# This simulates credential compromise

# Using smbclient
smbclient //192.168.1.10/C$ -U testuser%Password123!

# Or using RDP
xfreerdp /u:testuser /p:Password123! /v:192.168.1.10
```

## Step 3.5: Lateral Movement Simulation

```bash
# If you have multiple Windows machines, run:
crackmapexec smb 192.168.1.10 192.168.1.11 192.168.1.12 -u testuser -p Password123!

# This authenticates to multiple hosts = Lateral Movement
```

---

# PHASE 4: Detect in Splunk

## Step 4.1: Search for Failed Logins (4625)

**Splunk Web → Search & Reporting:**

```spl
index=main sourcetype=WinEventLog:Security EventCode=4625
| stats count by Account_Name, Source_Network_Address, ComputerName
| where count > 5
| sort - count
```

## Step 4.2: Search for Successful Logins (4624)

```spl
index=main sourcetype=WinEventLog:Security EventCode=4624
| stats count by Account_Name, Source_Network_Address, Logon_Type
| sort - count
```

## Step 4.3: Correlate Brute Force + Success

```spl
index=main sourcetype=WinEventLog:Security (EventCode=4625 OR EventCode=4624)
| sort _time
| transaction Account_Name, Source_Network_Address maxspan=10m
| where eventcount > 5 AND match(EventCode, "4624")
| table _time, Account_Name, Source_Network_Address, eventcount, EventCode
```

## Step 4.4: Check for Privilege Assignment (4672)

```spl
index=main sourcetype=WinEventLog:Security EventCode=4672
| stats count by SubjectUserName, ComputerName
| sort - count
```

## Step 4.5: Full Kill Chain Detection

```spl
index=main sourcetype=WinEventLog:Security 
  (EventCode=4625 OR EventCode=4624 OR EventCode=4672)
| sort _time
| stats 
    count(eval(EventCode=4625)) as failed_attempts
    count(eval(EventCode=4624)) as successful_logins
    count(eval(EventCode=4672)) as privilege_events
    values(EventCode) as event_sequence
    by Account_Name, Source_Network_Address
| where failed_attempts > 5 AND successful_logins > 0
| table Account_Name, Source_Network_Address, failed_attempts, successful_logins, privilege_events
```

---

# PHASE 5: Create Splunk Alerts

## Step 5.1: Create Brute Force Alert

1. Go to **Settings → Searches, Reports, and Alerts**
2. Click **New Alert**
3. Configure:

| Field | Value |
|-------|-------|
| Search | `index=main sourcetype=WinEventLog:Security EventCode=4625 \| stats count by Account_Name, Source_Network_Address \| where count > 10` |
| Alert Type | Real-time |
| Trigger Condition | Number of Results > 0 |
| Trigger Action | Send email / Add to Notable Events |

## Step 5.2: Save Custom SPL Rules

**Go to Settings → Searches, Reports, and Alerts → New Alert:**

Use the SPL queries from `correlation-rules/splunk/` folder in this project.

---

# PHASE 6: Investigation Practice

## Step 6.1: When Alert Triggers

```spl
# Get full timeline for suspicious IP
index=main sourcetype=WinEventLog:Security Source_Network_Address="192.168.1.100"
| sort _time
| table _time, EventCode, Account_Name, ComputerName, Logon_Type
```

## Step 6.2: Check Account Activity

```spl
# All activity for compromised account
index=main sourcetype=WinEventLog:Security Account_Name="testuser"
| stats count by EventCode, ComputerName
| sort - count
```

## Step 6.3: Generate Investigation Report

```spl
# Export timeline for incident report
index=main sourcetype=WinEventLog:Security 
  (EventCode=4625 OR EventCode=4624 OR EventCode=4672)
  earliest=-1h
| sort _time
| table _time, EventCode, Account_Name, Source_Network_Address, ComputerName, Logon_Type
| outputcsv incident_timeline.csv
```

---

# 🎯 Practice Scenarios

## Scenario 1: Basic Brute Force Detection
1. From Kali, run Hydra against Windows Server
2. In Splunk, detect the 4625 events
3. Create alert for threshold

## Scenario 2: Credential Compromise
1. Run brute force
2. Login with correct password
3. Correlate failed + success in Splunk

## Scenario 3: Lateral Movement (Requires 2+ Windows Machines)
1. Compromise first machine
2. Use credentials to access second machine
3. Detect multi-host authentication pattern

## Scenario 4: Full Kill Chain
1. Brute force → Success → Multiple hosts → Admin login
2. Run kill chain SPL query
3. Document in incident report

---

# 📝 Quick Reference Commands

## Kali Linux

| Tool | Command |
|------|---------|
| Hydra RDP | `hydra -l testuser -P pass.txt rdp://TARGET` |
| Hydra SMB | `hydra -l testuser -P pass.txt smb://TARGET` |
| CrackMapExec | `crackmapexec smb TARGET -u USER -p PASS.txt` |
| SMB Connect | `smbclient //TARGET/C$ -U user%pass` |
| RDP Connect | `xfreerdp /u:user /p:pass /v:TARGET` |

## Windows Server (PowerShell)

| Task | Command |
|------|---------|
| Check Security Log | `Get-EventLog -LogName Security -Newest 20` |
| Filter 4625 | `Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625}` |
| Check Audit Policy | `auditpol /get /category:*` |
| List Users | `net user` |
| Check Connections | `netstat -an` |

## Splunk SPL

| Detection | Query |
|-----------|-------|
| Failed Logins | `index=main EventCode=4625 \| stats count by Account_Name` |
| Success Logins | `index=main EventCode=4624` |
| Privilege | `index=main EventCode=4672` |
| Timeline | `index=main \| sort _time \| table _time, EventCode, Account_Name` |

---

# ✅ Success Criteria

After completing this lab, you should be able to:

- [ ] Generate brute force traffic from Kali
- [ ] See Event ID 4625 in Windows Event Viewer
- [ ] See Event ID 4625 in Splunk
- [ ] Create correlation rule for brute force
- [ ] Detect successful login after brute force
- [ ] Create Splunk alert
- [ ] Write incident report

---

## 🚨 Important Notes

1. **Only practice in your own lab** - Never attack systems you don't own
2. **Network isolation** - Keep lab network separate from production
3. **Screenshots** - Take screenshots of each step for portfolio
4. **Document everything** - Write findings in incident report

---

**Created by: Amresh Kumar (@Ak-cybe)**  
**Lab Guide Version: 1.0**  
**Date: December 2025**
