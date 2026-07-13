import datetime
from pathlib import Path
from . import contest_database,file_variants
import nanoid

SCRIPT_DIR = Path(__file__).resolve().parent
SUBMISSIONS_DIR = SCRIPT_DIR / "submissions"
IMAGES_DIR = SUBMISSIONS_DIR / "attachments"
LAST_UPDATED_FILE = SUBMISSIONS_DIR / "last_updated"

SUBMISSIONS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# submissions structure:  {submission_id:{"attachments":[],"text":"","avg":0,"sum":0,"count":0}}
async def save_contest(name: str, submissions, contest_date):
    if contest_date is None:
        contest_date = datetime.date.today()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    with contest_database.get_session() as session:
        contest = contest_database.Contests(name=name, year=contest_date.year, date=contest_date)
        session.add(contest)
        session.flush()

        for submission in submissions.values():
            submission_row = contest_database.Submissions(
                contest_id=contest.id,
                author=submission["author"],
                text=submission["text"],
                avg=submission["avg"],
                sum=submission["sum"],
                count=submission["count"],
            )

            session.add(submission_row)
            session.flush()

            file_links = submission.get("filenames") # file links for non nextcord attachments
            if file_links is not None:
                for file_link in file_links:
                    attachment_row = contest_database.Attachments(
                        submission_id=submission_row.id,
                        filename= str(Path(file_link).relative_to(SUBMISSIONS_DIR.parent)),
                    )

                    session.add(attachment_row)
                    session.flush()
                    file_variants.create_file_variants(session, attachment_row)
            else:
                for i, attachment in enumerate(submission["attachments"]):

                    filepath = Path(IMAGES_DIR) / f"{attachment.filename}"
                    while filepath.exists():
                        filepath = Path(IMAGES_DIR) / f"{filepath.stem}{nanoid.generate(size=6)}{filepath.suffix}"

                    await attachment.save(filepath)

                    attachment_row = contest_database.Attachments(
                        submission_id=submission_row.id,
                        filename=attachment.filename,
                    )

                    session.add(attachment_row)
                    session.flush()
                    file_variants.create_file_variants(session, attachment_row)