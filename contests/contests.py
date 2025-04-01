import datetime
import json
import os
from pathlib import Path
import time
import nextcord
import nanoid
from pydantic import BaseModel, Field
import dataclasses
from contests import file_formatting

SUBMISSIONS_DIR = Path("contests/submissions").resolve()
LAST_UPDATED_FILE = SUBMISSIONS_DIR / "last_updated"


class Submission(BaseModel):
    author: str
    text: str
    avg: float
    sum: int
    count: int
    files: list[str]


class InfoFile(BaseModel):
    name: str = Field(alias="contest name")
    submissions: list[Submission]
    date: datetime.date


@dataclasses.dataclass
class Contest:
    contest_id: str
    name: str
    year: str
    date: datetime.date
    submissions: list[Submission]

    @property
    def month(self) -> str:
        return self.date.strftime("%B")

    def link(self, file: str) -> str:
        path = SUBMISSIONS_DIR / self.year / self.contest_id / file
        webp = path.with_suffix(".webp")

        if webp.is_file():
            return f"/submissions/{self.year}/{self.contest_id}/{webp.name}"
        return f"/submissions/{self.year}/{self.contest_id}/{file}"


class InMemoryCache:
    def __init__(self):
        self._contests = []
        self.load_from_disk()
        self.mtime = time.time()

    def load_from_disk(self):
        self._contests = []

        for file in SUBMISSIONS_DIR.rglob("info.json"):
            file: Path = file.resolve()
            json_string = file.read_text()
            info = InfoFile.model_validate_json(json_string)

            self._contests.append(Contest(
                contest_id=file.parent.name,
                name=info.name,
                year=file.parent.parent.name,
                date=info.date,
                submissions=info.submissions,
            ))

        self._contests.sort(key=lambda c: c.date, reverse=True)

    @property
    def contests(self):
        if LAST_UPDATED_FILE.stat().st_mtime > self.mtime:
            self.load_from_disk()
            self.mtime = time.time()

        return self._contests


async def save_contest(name: str, submissions: dict[int, dict[nextcord.Attachment, str, str, float, int, int]]): # {submission_id:{"attachments":[],"text":"","avg":0,"sum":0,"count":0}}
    contest_info = {'name': name, 'submissions': [], 'date':datetime.now().date().isoformat()}
    year = datetime.now().year

    save_dir = f"{SUBMISSIONS_DIR}/{year}/{nanoid.generate(size=7)}"
    while os.path.exists(save_dir):
        save_dir = f"{SUBMISSIONS_DIR}/{year}/{nanoid.generate(size=7)}"

    if not os.path.exists(SUBMISSIONS_DIR):
        os.mkdir(SUBMISSIONS_DIR)
    if not os.path.exists(os.path.join(SUBMISSIONS_DIR, f"{year}")):
        os.mkdir(os.path.join(SUBMISSIONS_DIR, f"{year}"))
    os.mkdir(save_dir)

    for submission in submissions.values():
        submission_r = {
            "author": submission["author"],
            "text": submission["text"],
            "avg": submission["avg"],
            "sum": submission["sum"],
            "count": submission["count"],
            "files": []
        }


        for i,attachment in enumerate(submission["attachments"]):
            filepath = Path(save_dir) / f"file_{i}_{attachment.filename}"
            await attachment.save(filepath)
            file_formatting.format_file(filepath)
            submission_r["files"].append(filepath.name)

        contest_info['submissions'].append(submission_r)

    print(os.path.abspath(f"{save_dir}/info.json"))
    with open(f"{save_dir}/info.json", "w") as info_file:
        info_file.write(json.dumps(contest_info, indent=4))

        if not Path(LAST_UPDATED_FILE).exists():
            with open(LAST_UPDATED_FILE,"w"): pass
        Path(LAST_UPDATED_FILE).touch()
