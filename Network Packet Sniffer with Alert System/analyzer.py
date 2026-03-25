import json
from collections import defaultdict
import time
from database import log_alert
from alerter import send_alert

with open('config.json', 'r') as f:
    config = json.load(f)

# Trackers
ip_port_tracker = defaultdict(set) # {src_ip: {dst_ports}}
ip_packet_tracker = defaultdict(int) # {src_ip: count}
start_time = time.time()

def analyze_packet(src_ip, dst_port, protocol, flags):
    global start_time
    
    current_time = time.time()
    if current_time - start_time > config['time_window']:
        # Reset trackers every time window
        ip_port_tracker.clear()
        ip_packet_tracker.clear()
        start_time = current_time

    # 1. Port Scan Detection
    if dst_port:
        ip_port_tracker[src_ip].add(dst_port)
        if len(ip_port_tracker[src_ip]) > config['port_scan_threshold']:
            description = f"Accessed {len(ip_port_tracker[src_ip])} unique ports in {config['time_window']}s"
            log_alert(src_ip, "Port Scan", description)
            send_alert("Port Scan", src_ip, description)
            # Reset tracker for this IP to avoid multiple alerts in same window
            ip_port_tracker[src_ip] = set()

    # 2. Flood Detection (e.g., SYN Flood)
    ip_packet_tracker[src_ip] += 1
    if ip_packet_tracker[src_ip] > config['flood_threshold']:
        description = f"Sent {ip_packet_tracker[src_ip]} packets in {config['time_window']}s"
        log_alert(src_ip, "Traffic Flood", description)
        send_alert("Traffic Flood", src_ip, description)
        # Reset tracker for this IP
        ip_packet_tracker[src_ip] = 0

if __name__ == '__main__':
    # Test logic
    analyze_packet("192.168.1.100", 80, "TCP", "S")
    print("Analyzer test complete.")
