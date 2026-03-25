import socket
import time

def simulate_ssh():
    print("Simulating SSH attack...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 2222))
        s.recv(1024)
        s.send(b"SSH-2.0-OpenSSH_8.2p1\r\n")
        time.sleep(1)
        s.close()
    except Exception as e:
        print(f"SSH Simulation Error: {e}")

def simulate_ftp():
    print("Simulating FTP attack...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 2121))
        print(s.recv(1024).decode())
        s.send(b"USER admin\r\n")
        print(s.recv(1024).decode())
        s.send(b"PASS 123456\r\n")
        print(s.recv(1024).decode())
        s.close()
    except Exception as e:
        print(f"FTP Simulation Error: {e}")

if __name__ == "__main__":
    while True:
        simulate_ssh()
        time.sleep(2)
        simulate_ftp()
        time.sleep(5)
