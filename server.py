from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/start_analysis", methods=["POST"])
def start_analysis():
    res = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    if os.path.exists("part_d/reports/output/report.json"):
        with open("part_d/reports/output/report.json") as f:
            report = json.load(f)
        return jsonify({"status": "completed", "report": report})
    else:
        return jsonify({"status": "error", "stdout": res.stdout, "stderr": res.stderr, "msg": "report.json not found"}), 500

@app.route("/cases", methods=["GET"])
def cases():
    if os.path.exists("part_d/reports/output/report.json"):
        with open("part_d/reports/output/report.json") as f:
            report = json.load(f)
        return jsonify(report.get("detections", []))
    return jsonify([])

@app.route("/cases/<case_id>", methods=["GET"])
def case_detail(case_id):
    if os.path.exists("part_d/reports/output/report.json"):
        with open("part_d/reports/output/report.json") as f:
            report = json.load(f)
        for case in report.get("detections", []):
            if case.get("case_id", "") == case_id:
                return jsonify(case)
        return jsonify({"error": "case not found"}), 404
    return jsonify({"error": "report.json not found"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
