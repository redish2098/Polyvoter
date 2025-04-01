import random
from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import json
from contests import contests
from website import text_formatting
from whitenoise import WhiteNoise
from pathlib import Path

CACHE = contests.InMemoryCache()

app = Flask(__name__, template_folder="templates")
app.jinja_env.filters["md"] = text_formatting.parse

app.wsgi_app = WhiteNoise(
    app.wsgi_app,
    root= Path("contests/submissions").absolute(),
    prefix = "submissions/",
    autorefresh=False,
    max_age=31536000
)

@app.route("/")
def home():
    return render_template("index.html", contests=CACHE.contests)

@app.route("/submission/<int:year>/<contest_id>/<submission_num>")
def submission_page(year, contest_id, submission_num):
    """ Render a page for an individual submission """
    contest_path = os.path.join(contests.SUBMISSIONS_DIR, str(year), contest_id)
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
                           author=submission.get("author", ""),
                           )

@app.route("/random_submission")
def random_image():
    all_contests = []

    for year in os.listdir(contests.SUBMISSIONS_DIR):
        year_path = os.path.join(contests.SUBMISSIONS_DIR, year)
        if os.path.isdir(year_path):
            for contest_id in os.listdir(year_path):
                contest_path = os.path.join(year_path, contest_id)
                info_file = os.path.join(contest_path, "info.json")
                if os.path.exists(info_file):
                    with open(info_file, "r", encoding="utf-8") as f:
                        contest_data = json.loads(f.read())

                    all_contests.extend([(year,contest_id,submission_num) for submission_num,data in enumerate(contest_data["submissions"])])


    random_submission = random.choice(all_contests)
    return redirect(url_for(
        "submission_page",
        year=random_submission[0],
        contest_id=random_submission[1],
        submission_num=random_submission[2]))

@app.route("/website/styles/<style>")
def website_styles(style):
    return send_from_directory(os.path.abspath("website/templates/styles"), style)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
