import socket
import threading
import paramiko
from db import SessionLocal, AttackLog
from utils import get_geolocation
import datetime

class HoneyPotServer(paramiko.ServerInterface):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def check_auth_password(self, username, password):
        print(f"SSH Login Attempt: {self.ip} - {username}:{password}")
        log_attack(self.ip, self.port, "SSH", username, password)
        return paramiko.AUTH_FAILED

def log_attack(ip, port, protocol, username=None, password=None, command=None):
    db = SessionLocal()
    geo = get_geolocation(ip)
    
    attack = AttackLog(
        ip_address=ip,
        port=port,
        protocol=protocol,
        username=username,
        password=password,
        command=command,
        city=geo.get("city"),
        country=geo.get("country"),
        latitude=geo.get("lat"),
        longitude=geo.get("lon"),
        timestamp=datetime.datetime.utcnow()
    )
    db.add(attack)
    db.commit()
    db.close()

def start_ssh_honeypot(host='0.0.0.0', port=2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    print(f"[*] SSH Honeypot listening on {host}:{port}")

    host_key = paramiko.RSAKey(filename='host.key')

    while True:
        try:
            client, addr = sock.accept()
            print(f"[*] Connection from {addr[0]}:{addr[1]}")
            
            transport = paramiko.Transport(client)
            transport.add_server_key(host_key)
            
            server = HoneyPotServer(addr[0], port)
            transport.start_server(server=server)
            
        except Exception as e:
            print(f"[-] SSH Error: {e}")

if __name__ == "__main__":
    start_ssh_honeypot()
