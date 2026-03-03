from flask import Flask, render_template, request, jsonify
from datetime import datetime
from main import generate_ai_response
from browser_service import main as run_playwright_main
from pathlib import Path
import json
import threading

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# generate ai json


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    start = data.get("start_date")
    end = data.get("end_date")
    holidays = data.get("holidays", [])
    content = data.get("content", "")

    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end, "%Y-%m-%d").date()
    except Exception:
        return jsonify({"error": "Invalid date format"}), 400

    ai_response = generate_ai_response(
        start_date=start_dt,
        end_date=end_dt,
        content=content,
        holidays=holidays,
    )

    return jsonify({"generated_json": json.loads(ai_response)})


# save final edited json


@app.route("/save_final", methods=["POST"])
def save_final():
    data = request.json
    start = data["start_date"]
    end = data["end_date"]
    edited_json = data["edited_json"]

    filename = f"{start}_{end}_internship_details.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(edited_json, f, indent=4)

    return jsonify({"status": "saved"})


# list saved internship files


@app.route("/internships")
def list_internships():
    files = list(Path(".").glob("*_internship_details.json"))
    return jsonify({"files": [f.name for f in files]})


# run automation using file


@app.route("/run_automation", methods=["POST"])
def run_automation():
    data = request.json
    internship_file = data["internship_file"]

    if not Path(internship_file).exists():
        return jsonify({"error": "File not found"}), 404

    def background_job():
        run_playwright_main(internship_file=internship_file)

    threading.Thread(target=background_job, daemon=True).start()

    return jsonify({"status": "started"})


if __name__ == "__main__":
    app.run(debug=True)
