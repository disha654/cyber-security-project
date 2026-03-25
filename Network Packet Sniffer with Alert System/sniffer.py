from scapy.all import sniff, IP, TCP, UDP, ICMP
from database import log_packet
from analyzer import analyze_packet
import threading
from datetime import datetime

socketio = None

def set_socketio(sio):
    global socketio
    socketio = sio

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        length = len(packet)
        protocol = "Other"
        src_port = 0
        dst_port = 0
        flags = ""

        if TCP in packet:
            protocol = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            flags = str(packet[TCP].flags)
        elif UDP in packet:
            protocol = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        elif ICMP in packet:
            protocol = "ICMP"

        # Log to SQLite
        log_packet(src_ip, dst_ip, src_port, dst_port, length, flags, protocol)
        
        # Analyze for anomalies
        analyze_packet(src_ip, dst_port, protocol, flags)
        
        # Emit to frontend
        if socketio:
            socketio.emit('new_packet', {
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'protocol': protocol,
                'length': length,
                'flags': flags,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })

def start_sniffing(iface=None):
    print(f"Starting sniffer on interface: {iface if iface else 'all'}")
    sniff(iface=iface, prn=packet_callback, store=0)
