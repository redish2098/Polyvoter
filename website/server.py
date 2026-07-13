from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
from contests import  contest_database
from contests.contest_database import Submissions, Contests, Attachments, get_session
from website import text_formatting
from whitenoise import WhiteNoise
from pathlib import Path
from flask_compress import Compress
from sqlalchemy.sql import func
from sqlalchemy import desc

app = Flask(__name__,template_folder="templates")
contest_database.init_app(app)
Compress(app)
app.jinja_env.filters["md"] = text_formatting.parse
app.wsgi_app = WhiteNoise(
    app.wsgi_app,
    root= Path("contests/submissions").absolute(),
    prefix = "submissions/",
    autorefresh=True,
    max_age=31536000
)

@app.route("/")
def home():
    with get_session() as session:
        contests = session.query(Contests).order_by(desc(Contests.date)).all()
        return render_template("index.html",contests=contests)

@app.route("/submission/<int:submission_id>")
def submission_page(submission_id):
    """ Render a page for an individual submission """
    with get_session() as session:
        submission = session.query(Submissions).where(Submissions.id == submission_id)
        if submission is None:
            return "Submission not found", 404
        submission = submission.first()
        return render_template("submission.html",submission=submission)


@app.route("/random_submission")
def random_image():
    with get_session() as session:
        random_submission = session.query(Submissions).order_by(func.random()).first()
        return redirect(url_for("submission_page",submission_id = random_submission.id))

@app.route("/website/styles/<style>")
def website_styles(style):
    return send_from_directory(os.path.abspath("website/templates/styles"), style)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
