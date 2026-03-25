# Secure Chat App

A real-time, end-to-end encrypted chat application designed for privacy-conscious communication. Built with security-first principles, this app ensures that only the sender and intended receiver can read messages.

## Features

- **End-to-End Encryption**: Uses a combination of RSA and AES encryption for secure message exchange.
- **Real-time Communication**: Powered by Socket.IO for instantaneous messaging.
- **Client-side Encryption**: Encryption/decryption is handled on the client side, meaning the server never sees the plaintext messages.
- **Encrypted Database Logs**: Stores encrypted messages, keys, and IVs for chat history.
- **User Authentication**: Simple username registration with public key sharing.

## Tech Stack

- **Backend**: Python (Flask, Flask-SocketIO)
- **Database**: SQLite (for persistent message history)
- **Frontend**: HTML5, CSS3, JavaScript (WebCrypto API)
- **Protocol**: WebSockets (via Socket.IO)

## Getting Started

1. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install flask flask-socketio
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the app at `http://localhost:5000`.

## Architecture

- **Registration**: On registration, the client generates an RSA key pair. The public key is shared with the server for others to use.
- **Messaging**: When sending a message, the client generates a one-time AES key, encrypts the message, then encrypts that AES key with the recipient's public key.
- **Storage**: Only the ciphertext and encrypted keys are stored in the database.
