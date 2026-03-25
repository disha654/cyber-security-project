import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request, Response

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from password_tool.strength_checker import evaluate_password
from password_tool.wordlist_generator import generate_wordlist

app = Flask(__name__)


def _collect_payload(data):
    data = data or {}
    return {
        "name": (data.get("name") or "").strip() or None,
        "pet": ((data.get("nickname") or data.get("pet") or "").strip() or None),
        "dob": (data.get("dob") or "").strip() or None,
        "keyword": (data.get("keyword") or "").strip() or None,
    }


@app.get("/api/health")
def health_check():
    return jsonify({"status": "ok"})


@app.post("/api/analyze")
def analyze_password_api():
    data = request.get_json(silent=True) or {}
    password = (data.get("password") or "").strip()

    if not password:
        return jsonify({"error": "Password is required."}), 400

    return jsonify(evaluate_password(password))


@app.post("/api/generate")
def generate_wordlist_api():
    payload = _collect_payload(request.get_json(silent=True))
    wordlist = sorted(generate_wordlist(**payload))

    if not wordlist:
        return jsonify({"error": "Provide at least one input value."}), 400

    return jsonify(
        {
            "count": len(wordlist),
            "filename": "wordlist.txt",
            "preview": wordlist[:25],
        }
    )


@app.post("/api/download")
def download_wordlist_api():
    payload = _collect_payload(request.get_json(silent=True))
    wordlist = sorted(generate_wordlist(**payload))

    if not wordlist:
        return jsonify({"error": "Provide at least one input value."}), 400

    output_text = "\n".join(wordlist) + "\n"
    headers = {"Content-Disposition": "attachment; filename=wordlist.txt"}
    return Response(output_text, headers=headers, mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)
