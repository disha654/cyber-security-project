# Cyber Security Projects Collection

A comprehensive collection of cybersecurity projects focused on threat detection, privacy protection, and security analysis. This repository contains 7 distinct projects, each designed for educational and research purposes.

## 📋 Project Overview

| # | Project | Technology | Purpose |
|---|---------|------------|---------|
| 1 | [Browser Extension to Block Trackers](#1-browser-extension-to-block-trackers) | JavaScript (Manifest V3) | Block web trackers and protect privacy |
| 2 | [Cyber Threat Intelligence Dashboard](#2-cyber-threat-intelligence-dashboard) | Flask + MongoDB | Aggregate threat intel from multiple sources |
| 3 | [HoneyPot Server](#3-honeypot-server-to-detect-attack-patterns) | Python + React | Detect and visualize attack patterns |
| 4 | [Linux Hardening Audit Tool](#4-linux-hardening-audit-tool) | Python | Audit Linux security against CIS Benchmarks |
| 5 | [Log File Analyzer](#5-log-file-analyzer-for-intrusion-detection) | Python + pandas | Detect intrusion patterns in logs |
| 6 | [SQL Injection Playground](#6-sql-injection-playground-with-detection-engine) | Flask + SQLite | Learn SQLi detection and prevention |
| 7 | [Steganography Tool](#7-steganography-tool-for-imagefile-hiding) | Python + customtkinter | Hide/extract data in images |

---

## 1. Browser Extension to Block Trackers

A modern, privacy-focused browser extension to block known tracking scripts and provide detailed analytics.

### Features
- **Block Known Trackers**: Pre-configured list of common tracking domains (Google Analytics, Facebook, DoubleClick, etc.)
- **Real-time Badge Counter**: Shows the number of trackers blocked on the current page
- **Analytics Dashboard**: View total blocked requests and a breakdown by domain
- **Whitelist Support**: Easily allow trackers for specific domains if needed
- **Privacy First**: All data is stored locally in your browser

### Installation
1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right corner)
3. Click on **Load unpacked**
4. Select the `Browser Extension to Block Trackers` folder
5. The extension icon should appear in your toolbar

### Project Structure
```
Browser Extension to Block Trackers/
├── manifest.json          # Extension configuration (Manifest V3)
├── background.js          # Service worker for tracking
├── rules.json             # Static blocking rules
├── dashboard/             # Analytics dashboard UI
└── popup/                 # Extension popup UI
```

📖 [View Full README](./Browser%20Extension%20to%20Block%20Trackers/README.md)

---

## 2. Cyber Threat Intelligence Dashboard

A real-time dashboard to aggregate threat intelligence from VirusTotal and AbuseIPDB.

### Features
- **Real-time Lookup**: Search IP addresses or domains
- **Multi-Source Analysis**: Fetches data from VirusTotal and AbuseIPDB
- **Dashboard**: Visualize lookup metrics and types
- **History**: Keep track of all past lookups with tagging
- **Export**: Export history to CSV or JSON
- **Tagging**: Add custom tags to Indicators of Compromise (IOCs)

### Requirements
- Python 3.8+
- MongoDB (Running on `localhost:27017` by default)
- API Keys for VirusTotal and AbuseIPDB

### Quick Start
```bash
cd "Cyber Threat Intelligence Dashboard"
pip install -r requirements.txt
# Configure .env file with your API keys
python app.py
```

### Project Structure
```
Cyber Threat Intelligence Dashboard/
├── app.py                 # Main Flask application
├── .env.example           # Environment variables template
├── requirements.txt
├── services/
│   ├── api_client.py      # API integration logic
│   └── db.py              # MongoDB interaction
├── templates/             # HTML templates
└── static/                # CSS/JS assets
```

📖 [View Full README](./Cyber%20Threat%20Intelligence%20Dashboard/README.md)

---

## 3. HoneyPot Server to Detect Attack Patterns

A functional honeypot server to simulate vulnerable SSH and FTP services, logging attacker activities and visualizing them on a modern dashboard.

### Features
- **SSH Honeypot (Port 2222)**: Simulates an SSH server, logging login attempts and credentials
- **FTP Honeypot (Port 2121)**: Simulates an FTP server, logging login attempts
- **Real-time Dashboard**: Built with React with live attack feed
- **Geolocation**: Integrates with `ip-api.com` for attacker IP mapping
- **Dark Mode UI**: Modern, security-focused aesthetic with glassmorphism

### Quick Start
**Backend:**
```bash
cd "HoneyPot Server to Detect Attack Patterns/backend"
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd "HoneyPot Server to Detect Attack Patterns/frontend"
npm install
npm run dev
```

### Project Structure
```
HoneyPot Server to Detect Attack Patterns/
├── backend/
│   ├── main.py            # Main server entry point
│   ├── honeypot_ssh.py    # SSH honeypot
│   ├── honeypot_ftp.py    # FTP honeypot
│   └── db.py              # Database interaction
├── frontend/              # React dashboard
└── simulate_attacks.py    # Attack simulation script
```

📖 [View Full README](./HoneyPot%20Server%20to%20Detect%20Attack%20Patterns/README.md)

---

## 4. Linux Hardening Audit Tool

A Python-based utility to audit Linux system security configurations against CIS Benchmarks.

### Features
- **Filesystem Audit**: Checks permissions of critical files (`/etc/shadow`, `/etc/passwd`)
- **SSH Hardening**: Verifies secure SSH configurations
- **Network Security**: Audits kernel parameters (`sysctl`) and firewall status
- **Service Audit**: Identifies active vulnerable or unnecessary services
- **Rootkit Detection**: Scans for common rootkit indicators
- **Compliance Scoring**: Generates a percentage-based score and detailed report

### Usage
```bash
cd "Linux Hardening Audit Tool"
sudo python3 linux_audit.py
```

### Project Structure
```
Linux Hardening Audit Tool/
├── linux_audit.py         # Main audit script
├── requirements.txt
└── audit_report.json      # Generated audit report
```

📖 [View Full README](./Linux%20Hardening%20Audit%20Tool/README.md)

---

## 5. Log File Analyzer for Intrusion Detection

A Python-based tool to analyze Apache and SSH logs for suspicious activity, including brute-force attacks, DoS attempts, and vulnerability scanning.

### Features
- **Log Parsing**: Supports Apache Access Logs and SSH Authentication Logs
- **Threat Detection**:
  - **Brute Force**: Detects high frequency of failed SSH logins
  - **DoS Detection**: Flags IPs with unusually high request rates
  - **Vulnerability Scanning**: Identifies suspicious path access
  - **Blacklist Check**: Cross-references IPs against threat intelligence
- **Reporting**: Exports CSV alerts and generates visualization charts

### Quick Start
```bash
cd "Log File Analyzer for Intrusion Detection"
pip install -r requirements.txt
python app.py
```

### Project Structure
```
Log File Analyzer for Intrusion Detection/
├── app.py                 # Main application
├── analyzer.py            # Core analysis logic
├── parser.py              # Log parsing utilities
├── blacklist.py           # Threat intelligence blacklist
├── visualizer.py          # Chart generation
├── logs/                  # Sample log files
└── reports/               # Generated alerts and charts
```

📖 [View Full README](./Log%20File%20Analyzer%20for%20Intrusion%20Detection/README.md)

---

## 6. SQL Injection Playground with Detection Engine

An educational platform for understanding, detecting, and preventing SQL Injection attacks.

### Features
- **Real-Time Detection Engine (WAF-like)**: Monitors requests and identifies SQLi patterns
- **Interactive Playground**: Explore vulnerable endpoints for Search and Login
- **Live Security Dashboard**: View detected attacks with severity levels
- **Parameterized Protection**: Demonstrate prepared statements
- **Attacker Suite**: Simulate multiple SQLi attack types (Boolean, Union, Error-based)

### Quick Start
```bash
cd "SQL Injection Playground with Detection Engine"
pip install -r requirements.txt
python init_db.py
python app.py
# In another terminal:
python attacker.py
```

### Project Structure
```
SQL Injection Playground with Detection Engine/
├── app.py                 # Flask application
├── attacker.py            # Attack simulation script
├── detector.py            # SQLi detection engine
├── init_db.py             # Database initialization
└── logs/                  # Detection logs
```

📖 [View Full README](./SQL%20Injection%20Playground%20with%20Detection%20Engine/README.md)

---

## 7. Steganography Tool for Image/File Hiding

A modern GUI tool to hide and extract text or files within images using Least Significant Bit (LSB) steganography.

### Features
- **Modern UI**: Built with `customtkinter` for a sleek, dark-themed interface
- **Drag-and-Drop**: Easily drop images to encode or decode
- **LSB Encoding**: Uses the `stepic` library to embed data invisibly
- **Format Support**: Supports PNG and BMP (PNG recommended)

### Quick Start
```bash
cd "Steganography Tool for Image/File Hiding"
pip install -r requirements.txt
python app.py
```

### Project Structure
```
Steganography Tool for Image/File Hiding/
├── app.py                 # Main GUI application
├── stego_engine.py        # Core LSB steganography logic
└── requirements.txt
```

📖 [View Full README](./Steganography%20Tool%20for%20ImageFile%20Hiding/README.md)

---

## 🛡️ Security Disclaimer

These projects are designed for **educational and research purposes only**. 

- **Do not deploy** vulnerable projects (SQL Injection Playground, HoneyPot) in production environments
- Always test security tools in **controlled environments**
- Ensure you have **proper authorization** before testing on any system you don't own
- The HoneyPot should be run in an **isolated network** to prevent potential abuse

## 📚 Learning Objectives

This collection covers key cybersecurity domains:

- **Privacy Protection**: Browser extension for tracker blocking
- **Threat Intelligence**: CTI dashboard for IOC analysis
- **Attack Detection**: Honeypot and log analysis tools
- **Security Hardening**: Linux audit tool for compliance
- **Web Security**: SQL injection understanding and prevention
- **Data Protection**: Steganography for covert communication

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or suggest improvements
- Add new detection rules or features
- Improve documentation
- Add new security projects

## 📄 License

This project collection is for educational purposes. Individual projects may have their own licensing terms - please refer to each project's documentation.

## 👤 Author

**Disha**  
GitHub: [@disha654](https://github.com/disha654)

---

*Last Updated: March 2026*
