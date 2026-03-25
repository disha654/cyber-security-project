from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import sqlalchemy
from db import get_db, AttackLog
from honeypot_ssh import start_ssh_honeypot
from honeypot_ftp import start_ftp_honeypot
import threading
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Start honeypots in separate threads
    ssh_thread = threading.Thread(target=start_ssh_honeypot, daemon=True)
    ftp_thread = threading.Thread(target=start_ftp_honeypot, daemon=True)
    ssh_thread.start()
    ftp_thread.start()
    print("Honeypots started.")

BANNED_IPS = set()

@app.get("/api/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(AttackLog).order_by(AttackLog.timestamp.desc()).limit(100).all()

@app.get("/api/banned")
def get_banned():
    return list(BANNED_IPS)

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_attacks = db.query(AttackLog).count()
    unique_ips = db.query(AttackLog.ip_address).distinct().count()
    
    # Simple logic to "ban" IPs with more than 10 attempts
    recent_attacks = db.query(AttackLog.ip_address).group_by(AttackLog.ip_address).having(sqlalchemy.func.count(AttackLog.id) > 10).all()
    for ip in recent_attacks:
        BANNED_IPS.add(ip[0])
    
    return {
        "total_attacks": total_attacks,
        "unique_ips": unique_ips,
        "banned_count": len(BANNED_IPS)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
