import sqlite3
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

def init_db():
    conn = sqlite3.connect(config['db_path'])
    cursor = conn.cursor()
    
    # Packet log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS packet_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            src_ip TEXT,
            dst_ip TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            length INTEGER,
            flags TEXT,
            protocol TEXT
        )
    ''')
    
    # Alert log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alert_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            src_ip TEXT,
            alert_type TEXT,
            description TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_packet(src_ip, dst_ip, src_port, dst_port, length, flags, protocol):
    conn = sqlite3.connect(config['db_path'])
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO packet_logs (src_ip, dst_ip, src_port, dst_port, length, flags, protocol)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (src_ip, dst_ip, src_port, dst_port, length, flags, protocol))
    conn.commit()
    conn.close()

def log_alert(src_ip, alert_type, description):
    conn = sqlite3.connect(config['db_path'])
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO alert_logs (src_ip, alert_type, description)
        VALUES (?, ?, ?)
    ''', (src_ip, alert_type, description))
    conn.commit()
    conn.close()

def get_recent_packets(limit=100):
    conn = sqlite3.connect(config['db_path'])
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM packet_logs ORDER BY timestamp DESC LIMIT ?', (limit,))
    data = cursor.fetchall()
    conn.close()
    return data

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
