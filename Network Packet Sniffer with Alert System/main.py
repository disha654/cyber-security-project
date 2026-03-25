import threading
import sys
from database import init_db
from sniffer import start_sniffing
from visualizer import start_visualization
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description='Network Packet Sniffer with Alert System')
    parser.add_argument('--iface', type=str, help='Interface to sniff on')
    parser.add_argument('--no-graph', action='store_true', help='Disable live graph')
    args = parser.parse_args()

    # 1. Initialize DB
    print("[+] Initializing database...")
    init_db()

    # 2. Start Sniffer in a background thread
    print("[+] Starting packet sniffer thread...")
    sniff_thread = threading.Thread(target=start_sniffing, args=(args.iface,), daemon=True)
    sniff_thread.start()

    # 3. Start Visualization if requested
    if not args.no_graph:
        print("[+] Starting live visualization...")
        try:
            start_visualization()
        except KeyboardInterrupt:
            print("\n[-] Visualizer stopped.")
    else:
        print("[+] Sniffer running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[-] Sniffer stopped.")

if __name__ == '__main__':
    main()
