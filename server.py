from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/start_analysis", methods=["POST"])
def start_analysis():
    # Replace "python3 main.py" with your actual detection pipeline run
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    return jsonify({"status": "completed", "stdout": result.stdout, "stderr": result.stderr})

@app.route("/cases", methods=["GET"])
def cases():
    return jsonify([
        {
            "id": "CASE-001",
            "title": "Test Run",
            "score": 88,
            "range": "2025-11-16 13:00 → 13:10",
            "pcapsMB": 2,
            "investigator": "Hackathon Team",
            "uploaded": "2025-11-16T13:11Z"
        }
    ])

@app.route("/cases/<case_id>", methods=["GET"])
def case_detail(case_id):
    return jsonify({
        "id": case_id,
        "title": "Test Run",
        "score": 88,
        "timeline": [
            {"t": "13:01:00", "event": "Flow start", "volume": 120}
        ],
        "confidenceFactors": [
            {"name": "Timing", "score": 90, "details": "ok"}
        ],
        "packets": [
            {"time": "13:01:02", "src": "127.0.0.1", "dst": "10.0.0.2", "proto": "TCP", "len": 512, "flag": "candidate"}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

