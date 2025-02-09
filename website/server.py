import random

from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

IMAGE_FOLDER = os.path.abspath("contests/submissions")  # Ensure cross-platform compatibility


@app.route("/")
def home():
    contests = []

    # Scan the submissions folder to find years and contests
    for year in os.listdir(IMAGE_FOLDER):
        year_path = os.path.join(IMAGE_FOLDER, year)
        if os.path.isdir(year_path):
            for contest_id in os.listdir(year_path):
                contest_path = os.path.join(year_path, contest_id)
                info_file = os.path.join(contest_path, "info.json")

                if os.path.exists(info_file):
                    try:
                        with open(info_file, "r", encoding="utf-8") as f:
                            contest_data = json.load(f)
                        contests.append({
                            "year": year,
                            "contest_id": contest_id,
                            "contest_name": contest_data.get("contest name", "Unknown Contest"),
                            "submissions": contest_data.get("submissions", [])
                        })
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error reading {info_file}: {e}")

    return render_template("index.html", contests=contests)


@app.route("/submissions/<int:year>/<contest_id>/<filename>")
def serve_image(year, contest_id, filename):
    contest_path = os.path.join(IMAGE_FOLDER, str(year), contest_id)
    file_path = os.path.join(contest_path, filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    return send_from_directory(contest_path, filename)


@app.route("/submission/<int:year>/<contest_id>/<submission_num>")
def submission_page(year, contest_id, submission_num):
    """ Render a page for an individual submission """
    contest_path = os.path.join(IMAGE_FOLDER, str(year), contest_id)
    info_file = os.path.join(contest_path, "info.json")

    if not os.path.exists(info_file):
        return "Contest not found", 404

    with open(info_file, "r", encoding="utf-8") as f:
        contest_data = json.load(f)

    submission = contest_data["submissions"][int(submission_num)]


    if not submission:
        return "Submission not found", 404

    return render_template("submission.html",
                           year=year,
                           contest_id=contest_id,
                           text=submission.get("text", ""),
                           files=submission.get("files", []),
                           avg=submission.get("avg", "N/A"),
                           sum=submission.get("sum", "N/A"),
                           count=submission.get("count", "N/A"),
                           )

@app.route("/random_submission")
def random_image():
    contests = []

    for year in os.listdir(IMAGE_FOLDER):
        year_path = os.path.join(IMAGE_FOLDER, year)
        if os.path.isdir(year_path):
            for contest_id in os.listdir(year_path):
                contest_path = os.path.join(year_path, contest_id)
                info_file = os.path.join(contest_path, "info.json")
                if os.path.exists(info_file):
                    with open(info_file, "r", encoding="utf-8") as f:
                        contest_data = json.loads(f.read())

                    contests.extend([(year,contest_id,submission_num) for submission_num,data in enumerate(contest_data["submissions"])])


    random_submission = random.choice(contests)
    return redirect(url_for(
        "submission_page",
        year=random_submission[0],
        contest_id=random_submission[1],
        submission_num=random_submission[2]))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
