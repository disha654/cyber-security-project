# Cyber Security Projects Collection

A comprehensive collection of cybersecurity projects focused on threat detection, privacy protection, security analysis, and defensive training. This repository contains **15 distinct projects** covering various domains of cyber security.

## 📋 Complete Project List

| # | Project | Technology | Category |
|---|---------|------------|----------|
| 1 | [Browser Extension to Block Trackers](#browser-extension-to-block-trackers) | JavaScript (Manifest V3) | Privacy |
| 2 | [Cyber Threat Intelligence Dashboard](#cyber-threat-intelligence-dashboard) | Flask + MongoDB | Threat Intelligence |
| 3 | [Ethical Phishing Simulation Platform](#ethical-phishing-simulation-platform) | Full-stack | Security Awareness |
| 4 | [HoneyPot Server](#honeypot-server-to-detect-attack-patterns) | Python + React | Attack Detection |
| 5 | [Keylogger with Encrypted Data Exfiltration](#keylogger-with-encrypted-data-exfiltration) | Python | Defensive PoC |
| 6 | [Linux Hardening Audit Tool](#linux-hardening-audit-tool) | Python | Security Hardening |
| 7 | [Log File Analyzer](#log-file-analyzer-for-intrusion-detection) | Python + pandas | Intrusion Detection |
| 8 | [Network Packet Sniffer](#network-packet-sniffer-with-alert-system) | Python + Web Dashboard | Network Security |
| 9 | [Password Security Toolkit](#password-security-toolkit) | Next.js + Flask | Authentication |
| 10 | [Personal Firewall](#personal-firewall) | Python + Scapy | Network Defense |
| 11 | [Secure Chat App](#secure-chat-app) | Flask-SocketIO + WebCrypto | Secure Communication |
| 12 | [Secure File Storage System](#secure-file-storage-system-with-aes) | Python + AES-256-GCM | Data Protection |
| 13 | [SQL Injection Playground](#sql-injection-playground-with-detection-engine) | Flask + SQLite | Web Security |
| 14 | [Steganography Tool](#steganography-tool-for-imagefile-hiding) | Python + customtkinter | Data Hiding |
| 15 | [Web Application Vulnerability Scanner](#web-application-vulnerability-scanner) | Python | Security Testing |

---

## Projects

### Browser Extension to Block Trackers

A modern, privacy-focused browser extension to block known tracking scripts and provide detailed analytics.

**Features:**
- Block Known Trackers (Google Analytics, Facebook, DoubleClick, etc.)
- Real-time Badge Counter showing blocked trackers
- Analytics Dashboard with request breakdown
- Whitelist Support for specific domains
- Privacy First - all data stored locally

**Installation:**
1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode**
3. Click **Load unpacked** and select the project folder

📖 [Full Documentation](./Browser%20Extension%20to%20Block%20Trackers/README.md)

---

### Cyber Threat Intelligence Dashboard

A real-time dashboard to aggregate threat intelligence from VirusTotal and AbuseIPDB.

**Features:**
- Real-time IP and domain lookups
- Multi-source analysis (VirusTotal, AbuseIPDB)
- Historical tracking with tagging
- Export to CSV/JSON
- Visual dashboard for IOC metrics

**Quick Start:**
```bash
cd "Cyber Threat Intelligence Dashboard"
pip install -r requirements.txt
python app.py
```

📖 [Full Documentation](./Cyber%20Threat%20Intelligence%20Dashboard/README.md)

---

### Ethical Phishing Simulation Platform

A full-stack platform for conducting controlled phishing simulations to aid in security awareness training.

**Features:**
- Campaign management
- Custom email templates
- Real-time tracking of clicks and submissions
- User engagement analytics
- Safe, controlled environment for training

📖 [Full Documentation](./Ethical%20Phishing%20Simulation%20Platform/README.md)

---

### HoneyPot Server to Detect Attack Patterns

A functional honeypot server simulating vulnerable SSH and FTP services with a modern React dashboard.

**Features:**
- SSH Honeypot (Port 2222) - logs login attempts and credentials
- FTP Honeypot (Port 2121) - logs login attempts
- Real-time React dashboard with live attack feed
- Geolocation mapping via ip-api.com
- Dark mode UI with glassmorphism design

**Quick Start:**
```bash
# Backend
cd "HoneyPot Server to Detect Attack Patterns/backend"
pip install -r requirements.txt
python main.py

# Frontend (separate terminal)
cd "HoneyPot Server to Detect Attack Patterns/frontend"
npm install
npm run dev
```

📖 [Full Documentation](./HoneyPot%20Server%20to%20Detect%20Attack%20Patterns/README.md)

---

### Keylogger with Encrypted Data Exfiltration

A safe, synthetic event logger designed for defensive PoC training.

**Features:**
- Synthetic keyboard event generation
- Fernet encryption for logged data
- Simulated exfiltration to localhost-only receiver
- Demonstrates threat operation patterns
- Educational tool for defensive security

📖 [Full Documentation](./Keylogger%20with%20Encrypted%20Data%20Exfiltration/README.md)

---

### Linux Hardening Audit Tool

A Python-based utility to audit Linux system security configurations against CIS Benchmarks.

**Features:**
- Filesystem audit (permissions on /etc/shadow, /etc/passwd)
- SSH hardening verification
- Network security checks (sysctl, firewall)
- Service audit for vulnerable services
- Rootkit detection scanning
- Compliance scoring with recommendations

**Usage:**
```bash
cd "Linux Hardening Audit Tool"
sudo python3 linux_audit.py
```

📖 [Full Documentation](./Linux%20Hardening%20Audit%20Tool/README.md)

---

### Log File Analyzer for Intrusion Detection

A Python-based tool to analyze Apache and SSH logs for suspicious activity.

**Features:**
- Log parsing for Apache and SSH
- Brute force detection (failed SSH logins)
- DoS detection (high request rates)
- Vulnerability scanning detection
- Blacklist cross-referencing
- CSV alerts and PNG visualizations

**Quick Start:**
```bash
cd "Log File Analyzer for Intrusion Detection"
pip install -r requirements.txt
python app.py
```

📖 [Full Documentation](./Log%20File%20Analyzer%20for%20Intrusion%20Detection/README.md)

---

### Network Packet Sniffer with Alert System

A real-time network monitoring tool that captures traffic and provides a live web-based dashboard.

**Features:**
- Real-time packet capture
- Protocol analysis
- Live web dashboard for visualization
- Integrated alert system for suspicious activity
- Network traffic statistics

📖 [Full Documentation](./Network%20Packet%20Sniffer%20with%20Alert%20System/README.md)

---

### Password Security Toolkit

A Next.js and Flask-based toolkit for password security analysis and testing.

**Features:**
- Robust password strength analyzer
- Custom wordlist generator
- Password auditing capabilities
- Modern Next.js frontend
- Flask backend API

📖 [Full Documentation](./Password%20tool/README.md)

---

### Personal Firewall

A lightweight Python-based firewall using Scapy for packet inspection.

**Features:**
- JSON-based rule definitions
- Block/allow traffic by IP, port, protocol
- CLI interface
- Tkinter GUI
- Real-time packet inspection with Scapy

📖 [Full Documentation](./Personal%20Firewall/README.md)

---

### Secure Chat App

An end-to-end encrypted (E2EE) messaging application.

**Features:**
- RSA key exchange
- AES message encryption
- Real-time messaging with Flask-SocketIO
- WebCrypto API integration
- Only participants can read conversations

📖 [Full Documentation](./Secure%20Chat%20App/README.md)

---

### Secure File Storage System with AES

A local file encryption utility using AES-256-GCM.

**Features:**
- AES-256-GCM encryption
- Password-based key derivation (scrypt)
- Metadata protection
- Integrity verification
- Confidential file storage

📖 [Full Documentation](./Secure%20File%20Storage%20System%20with%20AES/README.md)

---

### SQL Injection Playground with Detection Engine

An educational platform for understanding, detecting, and preventing SQL Injection attacks.

**Features:**
- Real-time WAF-like detection engine
- Interactive vulnerable endpoints
- Live security dashboard
- Parameterized protection examples
- Attacker suite for simulation (Boolean, Union, Error-based)

**Quick Start:**
```bash
cd "SQL Injection Playground with Detection Engine"
pip install -r requirements.txt
python init_db.py
python app.py
# In another terminal:
python attacker.py
```

📖 [Full Documentation](./SQL%20Injection%20Playground%20with%20Detection%20Engine/README.md)

---

### Steganography Tool for Image/File Hiding

A modern GUI tool to hide and extract text or files within images using LSB steganography.

**Features:**
- Modern dark-themed UI with customtkinter
- Drag-and-drop image support
- LSB encoding using stepic library
- PNG and BMP format support
- Invisible data embedding

**Quick Start:**
```bash
cd "Steganography Tool for Image/File Hiding"
pip install -r requirements.txt
python app.py
```

📖 [Full Documentation](./Steganography%20Tool%20for%20ImageFile%20Hiding/README.md)

---

### Web Application Vulnerability Scanner

A DAST (Dynamic Application Security Testing) tool for identifying web application vulnerabilities.

**Features:**
- Web application crawling
- XSS vulnerability detection
- SQL Injection detection (error-based)
- Missing CSRF protection identification
- Automated security testing

📖 [Full Documentation](./Web%20Application%20Vulnerability%20Scanner/README.md)

---

## 🛠️ General Setup

Most projects in this collection are Python-based. To get started:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/disha654/cyber-security-project.git
   cd cyber-security-project
   ```

2. **Navigate to a specific project:**
   ```bash
   cd "Project Name"
   ```

3. **Install dependencies:**
   Use a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the project:**
   Follow specific instructions in each project's README.

---

## ⚖️ Ethical Use & Disclaimer

These tools are provided for **educational and ethical security testing purposes only**.

- **Do not** use these tools against any system or network without explicit, written authorization
- The authors and contributors are not responsible for any misuse or damage caused by these programs
- Always follow local laws and regulations regarding cyber security testing
- **Do not deploy** vulnerable projects (SQL Injection Playground, HoneyPot) in production environments
- Always test security tools in **controlled environments**
- Ensure you have **proper authorization** before testing on any system you don't own
- The HoneyPot should be run in an **isolated network** to prevent potential abuse

---

## 📚 Learning Objectives

This collection covers key cybersecurity domains:

- **Privacy Protection**: Browser extension, Steganography
- **Threat Intelligence**: CTI Dashboard, Log Analyzer
- **Attack Detection**: Honeypot, Network Sniffer, Vulnerability Scanner
- **Security Hardening**: Linux audit, Personal Firewall
- **Web Security**: SQL Injection Playground
- **Secure Communication**: E2EE Chat, File Encryption
- **Security Awareness**: Phishing Simulation
- **Defensive Training**: Keylogger PoC

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or suggest improvements
- Add new detection rules or features
- Improve documentation
- Add new security projects

---

## 📄 License

This project collection is for educational purposes. Individual projects may have their own licensing terms - please refer to each project's documentation.

---

## 👤 Author

**Disha**  
GitHub: [@disha654](https://github.com/disha654)

---

*Last Updated: March 2026*
