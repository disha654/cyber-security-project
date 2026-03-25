from flask import Flask, render_template, request, jsonify, send_file
from services.api_client import CTIClient
from services.db import DBManager
import os
import re
import pandas as pd
from io import BytesIO
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cti_secret_key")

api_client = CTIClient()
db_manager = DBManager()

def is_ip(target):
    # Basic regex for IPv4
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(ip_pattern, target) is not None

@app.route('/')
def index():
    metrics = db_manager.get_metrics()
    return render_template('index.html', metrics=metrics)

@app.route('/lookup', methods=['POST'])
def lookup():
    target = request.form.get('target', '').strip()
    if not target:
        return jsonify({"error": "No target provided"}), 400

    results = {}
    if is_ip(target):
        target_type = "IP"
        results['VirusTotal'] = api_client.lookup_ip_virustotal(target)
        results['AbuseIPDB'] = api_client.lookup_ip_abuseipdb(target)
    else:
        target_type = "Domain"
        results['VirusTotal'] = api_client.lookup_domain_virustotal(target)
        results['AbuseIPDB'] = {"error": "AbuseIPDB only supports IP lookups"}

    # Save to MongoDB
    db_manager.save_lookup(target, results, target_type)
    
    return jsonify({"target": target, "type": target_type, "results": results})

@app.route('/history')
def history():
    lookups = db_manager.get_all_lookups()
    return render_template('history.html', lookups=lookups)

@app.route('/tag', methods=['POST'])
def add_tag():
    data = request.json
    lookup_id = data.get('lookup_id')
    tag = data.get('tag')
    if lookup_id and tag:
        db_manager.add_tag(lookup_id, tag)
        return jsonify({"status": "success"})
    return jsonify({"error": "Missing lookup_id or tag"}), 400

@app.route('/export')
def export_data():
    lookups = db_manager.get_all_lookups()
    # Flatten data for export
    flattened_data = []
    for entry in lookups:
        row = {
            "target": entry["target"],
            "type": entry["target_type"],
            "timestamp": entry["timestamp"],
            "tags": ", ".join(entry.get("tags", []))
        }
        # Add basic scores if available
        vt = entry["results"].get("VirusTotal", {})
        abuse = entry["results"].get("AbuseIPDB", {})
        
        row["VT_Malicious"] = vt.get("malicious_count", 0)
        row["Abuse_Score"] = abuse.get("abuse_confidence_score", 0)
        flattened_data.append(row)

    df = pd.DataFrame(flattened_data)
    
    format = request.args.get('format', 'csv')
    if format == 'json':
        return jsonify(flattened_data)
    else:
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='cti_export.csv')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
