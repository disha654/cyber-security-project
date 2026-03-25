import json
import logging
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

with open('config.json', 'r') as f:
    config = json.load(f)

logging.basicConfig(filename=config['alert_log'], level=logging.INFO, format='%(asctime)s - %(message)s')

socketio = None

def set_socketio(sio):
    global socketio
    socketio = sio

def send_alert(alert_type, src_ip, description):
    message = f"ALERT: {alert_type} detected from source IP: {src_ip}. Description: {description}"
    
    # Log to file
    logging.info(message)
    print(f"\033[91m{message}\033[0m") # Red text in CLI
    
    # Emit to frontend
    if socketio:
        socketio.emit('new_alert', {
            'alert_type': alert_type,
            'src_ip': src_ip,
            'description': description,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Optional email alert
    if config['email_alerts']['enabled']:
        try:
            email_conf = config['email_alerts']
            msg = MIMEText(message)
            msg['Subject'] = f'Network Sniffer Alert: {alert_type}'
            msg['From'] = email_conf['sender_email']
            msg['To'] = email_conf['receiver_email']

            with smtplib.SMTP(email_conf['smtp_server'], email_conf['smtp_port']) as server:
                server.starttls()
                server.login(email_conf['sender_email'], email_conf['password'])
                server.send_message(msg)
            logging.info("Email alert sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send email alert: {e}")

if __name__ == '__main__':
    send_alert("Test Alert", "1.2.3.4", "Testing the alerting system")
