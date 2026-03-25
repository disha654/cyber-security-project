# Cyber Security Project Suite

A comprehensive collection of security tools and platforms designed for educational purposes, security research, and defensive training. This repository contains eight distinct projects covering various domains of cyber security, from network monitoring to end-to-end encrypted communication.

## 🚀 Projects Overview

### 1. [Ethical Phishing Simulation Platform](./Ethical%20Phishing%20Simulation%20Platform/)
A full-stack platform for conducting controlled phishing simulations. Features campaign management, custom email templates, and real-time tracking of clicks and submissions to aid in security awareness training.

### 2. [Network Packet Sniffer with Alert System](./Network%20Packet%20Sniffer%20with%20Alert%20System/)
A real-time network monitoring tool that captures traffic, analyzes protocols, and provides a live web-based dashboard for visualization. Includes an integrated alert system for detecting suspicious network activity.

### 3. [Secure Chat App](./Secure%20Chat%20App/)
An end-to-end encrypted (E2EE) messaging application. It utilizes RSA for key exchange and AES for message encryption, ensuring that only the participants can read the conversation. Built with Flask-SocketIO and the WebCrypto API.

### 4. [Keylogger with Encrypted Data Exfiltration](./Keylogger%20with%20Encrypted%20Data%20Exfiltration/)
A safe, synthetic event logger designed for defensive PoC training. It generates synthetic keyboard events, encrypts them using Fernet, and simulates exfiltration to a localhost-only receiver to demonstrate how such threats operate.

### 5. [Password Security Toolkit](./Password%20tool/)
A Next.js and Flask-based toolkit for password security. Features a robust password strength analyzer and a custom wordlist generator for authorized security testing and password auditing.

### 6. [Personal Firewall](./Personal%20Firewall/)
A lightweight Python-based firewall that uses Scapy for packet inspection. It allows users to define JSON-based rules to block or allow traffic based on IP, port, and protocol, featuring both a CLI and a Tkinter GUI.

### 7. [Secure File Storage System with AES](./Secure%20File%20Storage%20System%20with%20AES/)
A local file encryption utility using AES-256-GCM. It features password-based key derivation (scrypt), metadata protection, and integrity verification to ensure files remain confidential and untampered.

### 8. [Web Application Vulnerability Scanner](./Web%20Application%20Vulnerability%20Scanner/)
A DAST (Dynamic Application Security Testing) tool that crawls web applications to identify common vulnerabilities such as XSS, SQL Injection (error-based), and missing CSRF protections.

---

## 🛠️ General Setup

Most projects in this suite are Python-based. To get started generally:

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
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## ⚖️ Ethical Use & Disclaimer

These tools are provided for **educational and ethical security testing purposes only**. 
- **Do not** use these tools against any system or network without explicit, written authorization.
- The authors and contributors are not responsible for any misuse or damage caused by these programs.
- Always follow local laws and regulations regarding cyber security testing.

---
*Created as part of a Cyber Security Project portfolio.*
