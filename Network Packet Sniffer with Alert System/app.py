from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import sniffer
import alerter
from database import init_db
import json
import time

app = Flask(__name__)
# Using threading mode for better compatibility with scapy's native sockets
socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

# Connect socketio to modules
sniffer.set_socketio(socketio)
alerter.set_socketio(socketio)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    import sqlite3
    with open('config.json', 'r') as f:
        config = json.load(f)
    try:
        conn = sqlite3.connect(config['db_path'])
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM packet_logs")
        total_packets = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alert_logs")
        total_alerts = cursor.fetchone()[0]
        conn.close()
        return jsonify({
            'total_packets': total_packets,
            'total_alerts': total_alerts
        })
    except Exception as e:
        return jsonify({'error': str(e), 'total_packets': 0, 'total_alerts': 0})

def run_sniffer():
    sniffer.start_sniffing()

if __name__ == '__main__':
    init_db()
    # Start sniffer thread
    sniff_thread = threading.Thread(target=run_sniffer, daemon=True)
    sniff_thread.start()
    
    # Run Flask app
    print("Dashboard available at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
