import os
import json
import asyncio
from contests import contests, contest_database
import shutil

os.chdir('../contests')

async def import_legacy_contests():
    imported = 0
    print(contests.SUBMISSIONS_DIR)
    for info_path in contests.SUBMISSIONS_DIR.rglob("info.json"):
        print(f"Processing {info_path}")
        info_path = info_path.resolve()
        contest_folder = info_path.parent

        with open(info_path, "r") as f:
            info = json.load(f)

        submissions = {}
        for i, submission in enumerate(info["submissions"]):
            submissions[i] = {
                "author": submission["author"],
                "text": submission["text"],
                "avg": submission["avg"],
                "sum": submission["sum"],
                "count": submission["count"],
                "filenames": [
                    filename for filename in submission["files"]
                ],
            }

            new_files = []
            for filename in submissions[i]["filenames"]:
                new_path = contests.IMAGES_DIR / filename
                old_path = contest_folder / filename
                shutil.copy(old_path, new_path)
                new_files.append(new_path)

            submissions[i]["filenames"] = new_files

        contest_date = date_from_iso(info["date"])

        await contests.save_contest(
            name=info["contest name"],
            submissions=submissions,
            contest_date=contest_date,
        )
        imported += 1

    print(f"Imported {imported} contest(s).")

def date_from_iso(date_str: str):
    import datetime
    return datetime.date.fromisoformat(date_str)

if __name__ == "__main__":
    asyncio.run(import_legacy_contests())