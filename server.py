from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/start_analysis", methods=["POST"])
def start_analysis():
    res = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    git_push_result = ""
    detection_status = ""
    detections = []
    if os.path.exists("part_d/reports/output/report.json"):
        try:
            subprocess.run(["git", "add", "part_d/reports/output/report.json"])
            subprocess.run(["git", "commit", "-m", "Auto: update analysis output"], capture_output=True, text=True)
            push = subprocess.run(["git", "push"], capture_output=True, text=True)
            git_push_result = push.stdout + "\n" + push.stderr
        except Exception as e:
            git_push_result = str(e)
        with open("part_d/reports/output/report.json") as f:
            report = json.load(f)
        detections = report.get("detections", [])
        if not detections:
            detection_status = "NO_TOR"
        else:
            detection_status = "TOR"
        return jsonify({
            "status": "completed",
            "detection_status": detection_status,
            "report": report,
            "git_push": git_push_result,
            "stdout": res.stdout,
            "stderr": res.stderr
        })
    else:
        # File missing (timeout, error, etc)
        return jsonify({
            "status": "error",
            "detection_status": "NO_OUTPUT",
            "stdout": res.stdout,
            "stderr": res.stderr,
            "msg": "report.json not found"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)