# Linux Hardening Audit Tool

A Python-based utility to audit Linux system security configurations against CIS Benchmarks.

## Features

- **Filesystem Audit:** Checks permissions and ownership of critical files (`/etc/shadow`, `/etc/passwd`, etc.).
- **SSH Hardening:** Verifies secure SSH configurations (e.g., Root Login disabled, Max Auth Tries).
- **Network Security:** Audits kernel parameters (`sysctl`) and firewall status.
- **Service Audit:** Identifies active vulnerable or unnecessary services (e.g., Telnet, FTP).
- **Rootkit Detection:** Scans for common rootkit indicators and suspicious paths.
- **Compliance Scoring:** Generates a percentage-based score and detailed report.

## Requirements

- Python 3.x
- Root/Sudo privileges (for accessing system configuration files)

## How to Run

### 1. Transfer the script to your Linux machine
You can use `scp` or copy the content of `linux_audit.py` directly.

### 2. Run with Sudo
The script needs root access to read files like `/etc/shadow` and run `sysctl`.

```bash
sudo python3 linux_audit.py
```

### 3. View the Report
The script will output a summary to the console and save a detailed JSON report to `audit_report.json`.

## Compliance Score
The tool calculates a score based on the ratio of passed checks. Each failed check includes a **Recommendation** to fix the vulnerability.

## Disclaimer
This tool is for educational and auditing purposes. Always test hardening changes in a staging environment before applying them to production systems.
