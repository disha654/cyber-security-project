# HoneyPot Sentinel - Attack Pattern Detection

A functional honeypot server to simulate vulnerable SSH and FTP services, logging attacker activities and visualizing them on a modern dashboard.

## Features
- **SSH Honeypot (Port 2222):** Simulates an SSH server, logging login attempts and credentials.
- **FTP Honeypot (Port 2121):** Simulates an FTP server, logging login attempts.
- **Real-time Dashboard:** Built with React, featuring:
  - Total and Unique Attack counters.
  - Threats Blocked counter (Simulated Fail2Ban).
  - Live Attack Feed with IP, Protocol, and Geolocation.
  - Threat Intelligence summary.
- **Geolocation:** Integrates with `ip-api.com` for attacker IP mapping.
- **Dark Mode UI:** Modern, security-focused aesthetic with glassmorphism.

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm

### Backend Setup
1. Open a terminal in the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python main.py
   ```
   *Note: Honeypots will automatically start on ports 2222 (SSH) and 2121 (FTP).*

### Frontend Setup
1. Open another terminal in the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dashboard:
   ```bash
   npm run dev
   ```
4. Open `http://localhost:5173` in your browser.

### Simulating Attacks
To see the honeypot in action without real external traffic, run the simulation script:
```bash
python simulate_attacks.py
```

## Security Note
This is a demonstration honeypot. While it simulates vulnerable services, it is designed for monitoring and should be run in a controlled environment.
