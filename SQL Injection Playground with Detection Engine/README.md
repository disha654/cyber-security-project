# SQL Injection Playground with Real-Time Detection Engine

An educational platform for understanding, detecting, and preventing SQL Injection attacks.

## 🌟 Key Features
1. **Real-Time Detection Engine (WAF-like Middleware)**: Monitors every request to the application, identifies SQLi patterns, and logs them instantly.
2. **Interactive Playground**: Explore vulnerable endpoints for Search and Login, and see the raw SQL queries being executed.
3. **Live Security Dashboard**: View a history of detected attacks, including payloads, source IP, and severity.
4. **Parameterized Protection**: Demonstrate how prepared statements completely neutralize SQLi risks.
5. **Attacker Suite**: A dedicated script to simulate multiple types of SQLi attacks (Boolean, Union, Error, etc.).

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.x installed.

### 2. Setup
Install the necessary Python libraries:
```bash
pip install flask requests
```

### 3. Initialize Database
Create the SQLite database and seed it with dummy user data:
```bash
python init_db.py
```

### 4. Start the Application
Run the Flask server:
```bash
python app.py
```
Visit the playground at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 5. Launch the Attacker Suite (New Terminal)
While the application is running, execute the attack simulator:
```bash
python attacker.py
```

## 🛠️ Educational Exercises
- **Attack & Monitor**: Run `attacker.py` and then check the `/dashboard` in your browser to see how the detections were recorded in real-time.
- **Manual Exploitation**: Try to log in without a password using `' OR 1=1 --` on the vulnerable login form.
- **Analyze the Code**: 
    - Open `app.py` and look at the `detection_engine()` function to see the regex-based detection logic.
    - Compare `login()` (vulnerable) with `secure_login()` (protected) to understand the fix.

---
**Disclaimer**: This project is for educational purposes only. **Do not use this code in a production environment** as it is designed to be intentionally insecure.
