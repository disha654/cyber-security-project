from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from db import SessionLocal, AttackLog
from utils import get_geolocation
import datetime

class HoneyPotFTPHandler(FTPHandler):
    def on_login_failed(self, username, password):
        ip = self.remote_ip
        print(f"FTP Login Failed: {ip} - {username}:{password}")
        log_attack(ip, 2121, "FTP", username, password)

    def on_incomplete_login(self, username):
        # Handle cases where login isn't fully completed but username is sent
        pass

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

def start_ftp_honeypot(host='0.0.0.0', port=2121):
    authorizer = DummyAuthorizer()
    # No real users needed, we just want to log failed attempts
    
    handler = HoneyPotFTPHandler
    handler.authorizer = authorizer
    handler.banner = "vsFTPd 2.3.4" # Vulnerable-sounding banner

    server = FTPServer((host, port), handler)
    print(f"[*] FTP Honeypot listening on {host}:{port}")
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_honeypot()
