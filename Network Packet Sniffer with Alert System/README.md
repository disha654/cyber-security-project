# Network Packet Sniffer with Alert System

A powerful network monitoring tool that captures and analyzes network traffic in real-time. It includes a dashboard for live visualization of packet data and an integrated alert system for detecting potential security threats.

## Features

- **Real-time Packet Capture**: Sniffs network packets using multi-threading.
- **Protocol Analysis**: Supports TCP, UDP, ICMP, and common application layer protocols.
- **Interactive Dashboard**: A web-based visualizer for live traffic monitoring.
- **Alert System**: Logs and notifies users of suspicious network patterns.
- **Data Persistence**: Stores captured packet metadata in a SQLite database for further analysis.

## Tech Stack

- **Backend**: Python (threading, socket)
- **Visualization**: Python (Flask, Matplotlib/Dash)
- **Database**: SQLite
- **Network Stack**: Raw sockets or Scapy

## Getting Started

1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the sniffer:
   ```bash
   python main.py
   ```
3. Options:
   - `--iface`: Specify the network interface (e.g., `eth0`, `wlan0`).
   - `--no-graph`: Run in CLI mode without the visual dashboard.

## Security Warning

Packet sniffing requires administrative/root privileges on most operating systems. Use this tool only on networks where you have explicit permission to capture traffic.
