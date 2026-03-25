from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import time
import re
import logging
import os

app = Flask(__name__)

# Configure Logging
if not os.path.exists('logs'): os.makedirs('logs')
logging.basicConfig(filename='logs/sqli_detections.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Real-Time Detection Engine (Middleware)
@app.before_request
def detection_engine():
    sqli_patterns = [
        r"'.*--",                
        r"'.*OR.*=.*",           
        r"UNION.*SELECT",        
        r"SLEEP\(.*\)",          
        r"DROP.*TABLE",          
        r"benchmark\(.*\)",       
        r"information_schema"    
    ]
    
    params = {**request.args.to_dict(), **request.form.to_dict()}
    
    for key, value in params.items():
        for pattern in sqli_patterns:
            if re.search(pattern, str(value), re.IGNORECASE):
                log_msg = f"SQLi DETECTED! IP: {request.remote_addr}, Endpoint: {request.path}, Payload: {value}, Type: {pattern}"
                logging.warning(log_msg)
                try:
                    conn = get_db_connection()
                    conn.execute('INSERT INTO detections (source_ip, endpoint, payload, detection_type, severity) VALUES (?, ?, ?, ?, ?)',
                                (request.remote_addr, request.path, value, pattern, 'HIGH'))
                    conn.commit()
                    conn.close()
                except:
                    pass
                break 

# Modern Tailwind CSS Template
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQLi Shield | Security Playground</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="bg-slate-50 min-h-screen">
    <!-- Navbar -->
    <nav class="bg-slate-900 text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center">
                    <span class="text-emerald-400 text-2xl mr-2"><i class="fas fa-user-shield"></i></span>
                    <span class="font-bold text-xl tracking-tight">SQLi<span class="text-emerald-400">Shield</span></span>
                </div>
                <div class="flex space-x-4">
                    <a href="/" class="hover:bg-slate-800 px-3 py-2 rounded-md text-sm font-medium transition"><i class="fas fa-home mr-1"></i> Playground</a>
                    <a href="/dashboard" class="bg-emerald-600 hover:bg-emerald-700 px-4 py-2 rounded-md text-sm font-bold transition shadow-md"><i class="fas fa-terminal mr-1"></i> Live Monitor</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-5xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
        {{ content | safe }}

        {% if message %}
        <div class="mt-10 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center">
                <i class="fas fa-server text-slate-400 mr-2"></i>
                <h3 class="font-semibold text-slate-700 uppercase tracking-wider text-xs">Backend Response</h3>
            </div>
            <div class="p-6">
                <div class="p-4 {% if 'SUCCESS' in message or 'Found' in message %}bg-emerald-50 text-emerald-700 border-emerald-200{% elif 'Error' in message %}bg-rose-50 text-rose-700 border-rose-200{% else %}bg-slate-50 text-slate-700 border-slate-200{% endif %} rounded-lg border mb-4">
                    <p class="font-medium">{{ message }}</p>
                </div>
                {% if query %}
                <div>
                    <span class="text-xs font-bold text-slate-400 uppercase mb-2 block">Executed Query</span>
                    <pre class="bg-slate-900 text-emerald-400 p-4 rounded-lg overflow-x-auto font-mono text-sm border border-slate-800 shadow-inner"><code>{{ query }}</code></pre>
                </div>
                {% endif %}
            </div>
        </div>
        {% endif %}
    </main>

    <footer class="text-center py-10 text-slate-400 text-sm">
        <p>&copy; 2026 SQLi Shield Platform • Educational Cybersecurity Tool</p>
    </footer>
</body>
</html>
'''

INDEX_CONTENT = '''
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Search Card -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 transition hover:shadow-md">
            <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-rose-100 rounded-xl flex items-center justify-center text-rose-600 mr-4">
                    <i class="fas fa-search text-xl"></i>
                </div>
                <div>
                    <h2 class="text-xl font-bold text-slate-800">Vulnerable Search</h2>
                    <span class="text-xs font-bold text-rose-500 uppercase">Unprotected</span>
                </div>
            </div>
            <p class="text-slate-500 text-sm mb-6 leading-relaxed">Demonstrates <b>Union-based</b> or <b>Boolean-based</b> injection via string formatting.</p>
            <form action="/search" method="GET" class="space-y-4">
                <input type="text" name="role" placeholder="Enter role (e.g., user)" required 
                       class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 transition outline-none">
                <button type="submit" class="w-full bg-slate-800 hover:bg-slate-900 text-white font-bold py-3 rounded-xl transition transform active:scale-[0.98] shadow-sm">
                    Execute Search
                </button>
            </form>
        </div>

        <!-- Vulnerable Login -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 transition hover:shadow-md">
            <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-rose-100 rounded-xl flex items-center justify-center text-rose-600 mr-4">
                    <i class="fas fa-unlock-alt text-xl"></i>
                </div>
                <div>
                    <h2 class="text-xl font-bold text-slate-800">Vulnerable Login</h2>
                    <span class="text-xs font-bold text-rose-500 uppercase">Unprotected</span>
                </div>
            </div>
            <p class="text-slate-500 text-sm mb-6 leading-relaxed">Uses raw input to build the query. Try the classic <code>' OR 1=1 --</code> bypass.</p>
            <form action="/login" method="POST" class="space-y-4">
                <input type="text" name="username" placeholder="Username" required 
                       class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 transition outline-none">
                <input type="password" name="password" placeholder="Password" required 
                       class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 transition outline-none">
                <button type="submit" class="w-full bg-rose-600 hover:bg-rose-700 text-white font-bold py-3 rounded-xl transition transform active:scale-[0.98] shadow-md shadow-rose-200">
                    Bypass Login
                </button>
            </form>
        </div>
    </div>

    <!-- Secure Path -->
    <div class="mt-8 bg-emerald-900 rounded-2xl p-1 shadow-xl">
        <div class="bg-white rounded-[15px] p-8">
            <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-600 mr-4">
                    <i class="fas fa-shield-halved text-xl"></i>
                </div>
                <div>
                    <h2 class="text-xl font-bold text-slate-800">Secure Login</h2>
                    <span class="text-xs font-bold text-emerald-500 uppercase">Parameterized / Protected</span>
                </div>
            </div>
            <p class="text-slate-500 text-sm mb-6 leading-relaxed">This endpoint uses <b>Prepared Statements</b>. Injection attempts here will be treated as literal strings and safely ignored by the database.</p>
            <form action="/secure-login" method="POST" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <input type="text" name="username" placeholder="Username" required 
                       class="px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition outline-none">
                <input type="password" name="password" placeholder="Password" required 
                       class="px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition outline-none">
                <button type="submit" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 rounded-xl transition transform active:scale-[0.98] shadow-md shadow-emerald-200">
                    Secure Login
                </button>
            </form>
        </div>
    </div>
'''

DASHBOARD_CONTENT = '''
    <div class="bg-white rounded-2xl shadow-lg border border-slate-200 overflow-hidden">
        <div class="bg-slate-900 px-8 py-6 flex items-center justify-between">
            <div class="flex items-center">
                <div class="w-10 h-10 bg-emerald-500/20 rounded-lg flex items-center justify-center text-emerald-400 mr-4">
                    <i class="fas fa-pulse animate-pulse"></i>
                </div>
                <div>
                    <h2 class="text-white text-xl font-bold tracking-tight">Real-Time Threat Monitor</h2>
                    <p class="text-slate-400 text-xs uppercase tracking-widest font-semibold">Live WAF Detections</p>
                </div>
            </div>
            <div class="text-slate-400 text-sm">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-300">
                    Active
                </span>
            </div>
        </div>
        
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-50 text-slate-500 uppercase text-xs font-bold tracking-wider">
                        <th class="px-8 py-4">Timestamp</th>
                        <th class="px-6 py-4">Endpoint</th>
                        <th class="px-6 py-4">Payload</th>
                        <th class="px-6 py-4">Pattern</th>
                        <th class="px-6 py-4 text-right">Severity</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                    {% for det in detections %}
                    <tr class="hover:bg-slate-50 transition group">
                        <td class="px-8 py-5 text-slate-600 text-sm font-medium">{{ det.timestamp }}</td>
                        <td class="px-6 py-5"><span class="px-2 py-1 bg-slate-100 text-slate-700 rounded text-xs font-mono font-bold uppercase">{{ det.endpoint }}</span></td>
                        <td class="px-6 py-5"><code class="text-rose-600 bg-rose-50 px-2 py-1 rounded text-xs font-mono border border-rose-100">{{ det.payload }}</code></td>
                        <td class="px-6 py-5 text-slate-500 text-xs font-mono">{{ det.detection_type }}</td>
                        <td class="px-6 py-5 text-right">
                            <span class="px-3 py-1 bg-rose-600 text-white rounded-full text-[10px] font-black uppercase tracking-tighter">
                                {{ det.severity }}
                            </span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        {% if not detections %}
        <div class="p-20 text-center">
            <div class="text-slate-200 mb-4 text-6xl">
                <i class="fas fa-satellite-dish"></i>
            </div>
            <h3 class="text-slate-400 font-medium">Listening for suspicious activity...</h3>
            <p class="text-slate-300 text-sm mt-2">No threats detected in current session.</p>
        </div>
        {% endif %}
    </div>
    <div class="mt-6 flex justify-between items-center text-slate-400 text-xs">
        <p>Showing last 10 detections</p>
        <p>IP Resolution: Enabled</p>
    </div>
'''

@app.route('/')
def index():
    return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    detections = conn.execute('SELECT * FROM detections ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    content = render_template_string(DASHBOARD_CONTENT, detections=detections)
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/search')
def search():
    role = request.args.get('role', '')
    query = f"SELECT * FROM users WHERE role = '{role}'" 
    conn = get_db_connection()
    try:
        results = conn.execute(query).fetchall()
        conn.close()
        msg = f"Found {len(results)} matches for role '{role}'."
        return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT, message=msg, query=query)
    except Exception as e:
        return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT, message=f"Error: {e}", query=query)

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username', '')
    pw = request.form.get('password', '')
    query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{pw}'"
    conn = get_db_connection()
    try:
        res = conn.execute(query).fetchone()
        conn.close()
        if res: msg = f"SUCCESS: Welcome {res['username']} (Role: {res['role']})"
        else: msg = "FAILED: Invalid credentials."
        return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT, message=msg, query=query)
    except Exception as e:
        return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT, message=f"Error: {e}", query=query)

@app.route('/secure-login', methods=['POST'])
def secure_login():
    user = request.form.get('username', '')
    pw = request.form.get('password', '')
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    conn = get_db_connection()
    try:
        res = conn.execute(query, (user, pw)).fetchone()
        conn.close()
        if res: msg = f"SECURE SUCCESS: Welcome {res['username']}"
        else: msg = "SECURE FAILED: Invalid credentials."
        return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT, message=msg, query=f"{query} [Prepared Values: {user}, {pw}]")
    except Exception as e:
        return render_template_string(BASE_TEMPLATE, content=INDEX_CONTENT, message=f"Error: {e}", query=query)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
