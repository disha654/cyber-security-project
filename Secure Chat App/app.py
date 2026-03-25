from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app)

users = {}  # username -> {"public_key": str, "sid": str}

DB_DIR = Path("database")
DB_PATH = DB_DIR / "chat.db"

# ------------------ ROUTES ------------------

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

# ------------------ SOCKET EVENTS ------------------

@socketio.on('register_user')
def register_user(data):
    username = (data or {}).get('username')
    public_key = (data or {}).get('public_key')

    if not username or not public_key:
        emit('error', {'message': 'username and public_key are required'})
        return

    users[username] = {
        "public_key": public_key,
        "sid": request.sid,
    }
    print(f"{username} registered.")

@socketio.on('send_message')
def handle_message(data):
    payload = data or {}
    sender = payload.get('from')
    receiver = payload.get('to')
    encrypted_message = payload.get('encrypted_message')
    encrypted_key = payload.get('encrypted_key')
    iv = payload.get('iv')

    if not sender or not receiver or not encrypted_message or not encrypted_key or not iv:
        emit('error', {'message': 'invalid encrypted message payload'})
        return

    # Store encrypted log
    save_encrypted_message(payload)

    # Deliver only to sender and intended receiver, not broadcast to everyone
    sender_sid = users.get(sender, {}).get("sid")
    receiver_sid = users.get(receiver, {}).get("sid")

    if receiver_sid:
        emit('receive_message', payload, to=receiver_sid)
    if sender_sid and sender_sid != receiver_sid:
        emit('receive_message', payload, to=sender_sid)


@socketio.on('get_public_key')
def get_public_key(data):
    username = (data or {}).get('username')
    if not username:
        return {'public_key': None}
    return {'public_key': users.get(username, {}).get('public_key')}


@socketio.on('disconnect')
def on_disconnect():
    disconnected_user = None
    for username, entry in list(users.items()):
        if entry.get("sid") == request.sid:
            disconnected_user = username
            break
    if disconnected_user:
        users.pop(disconnected_user, None)

# ------------------ DATABASE ------------------

def save_encrypted_message(data):
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ensure_messages_schema(c)
    c.execute("""
        INSERT INTO messages (
            sender,
            receiver,
            encrypted_message,
            encrypted_key,
            encrypted_key_sender,
            iv
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data['from'],
        data['to'],
        data['encrypted_message'],
        data['encrypted_key'],
        data.get('encrypted_key_sender'),
        data['iv']
    ))
    conn.commit()
    conn.close()


def ensure_messages_schema(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            sender TEXT,
            receiver TEXT,
            encrypted_message TEXT,
            encrypted_key TEXT,
            iv TEXT
        )
    """)
    cursor.execute("PRAGMA table_info(messages)")
    existing_columns = {row[1] for row in cursor.fetchall()}

    if 'encrypted_key_sender' not in existing_columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN encrypted_key_sender TEXT")


@socketio.on('get_history')
def get_history(data):
    payload = data or {}
    username = payload.get('username')
    with_user = payload.get('with_user')
    if not username or not with_user:
        return {'messages': []}

    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ensure_messages_schema(c)
    c.execute("""
        SELECT sender, receiver, encrypted_message, encrypted_key, encrypted_key_sender, iv
        FROM messages
        WHERE (sender = ? AND receiver = ?)
           OR (sender = ? AND receiver = ?)
        ORDER BY rowid DESC
        LIMIT 200
    """, (username, with_user, with_user, username))
    rows = c.fetchall()
    conn.close()

    rows.reverse()
    messages = [
        {
            'from': row[0],
            'to': row[1],
            'encrypted_message': row[2],
            'encrypted_key': row[3],
            'encrypted_key_sender': row[4],
            'iv': row[5],
        }
        for row in rows
    ]
    return {'messages': messages}

if __name__ == '__main__':
    socketio.run(app, debug=True)
