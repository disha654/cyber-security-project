import sqlite3
import os

def init_db():
    if os.path.exists('database.db'):
        os.remove('database.db')
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Create detections table for real-time monitoring
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source_ip TEXT,
            endpoint TEXT,
            payload TEXT,
            detection_type TEXT,
            severity TEXT
        )
    ''')

    # Add dummy data
    users = [
        ('admin', 'adminpass', 'administrator'),
        ('alice', 'alicepass', 'user'),
        ('bob', 'bobpass', 'user')
    ]

    cursor.executemany('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', users)
    
    conn.commit()
    conn.close()
    print("Database initialized with 'users' and 'detections' tables.")

if __name__ == '__main__':
    init_db()
