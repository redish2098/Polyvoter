from flask import Flask, render_template, send_from_directory
import os
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

IMAGE_FOLDER = os.path.abspath("contests\\submissions")  # Base folder for contest submissions


@app.route("/")
def home():
    contests = []

    # Scan the submissions folder to find years and contests
    print(os.getcwd())
    for year in os.listdir(IMAGE_FOLDER):
        year_path = os.path.join(IMAGE_FOLDER, year)
        if os.path.isdir(year_path):
            for contest_id in os.listdir(year_path):
                contest_path = os.path.join(year_path, contest_id)
                info_file = os.path.join(contest_path, "info.json")

                if os.path.exists(info_file):
                    with open(info_file, "r", encoding="utf-8") as f:
                        contest_data = json.load(f)
                    contests.append({
                        "year": year,
                        "contest_id": contest_id,
                        "contest_name": contest_data["contest name"],
                        "submissions": contest_data["submissions"]
                    })

    return render_template("index.html", contests=contests)


@app.route("/submissions/<int:year>/<contest_id>/<filename>")
def serve_image(year, contest_id, filename):
    contest_path = os.path.join(IMAGE_FOLDER, str(year), contest_id)
    return send_from_directory(contest_path, filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
