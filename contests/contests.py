import datetime
import json
import os
from datetime import datetime
import nextcord
import nanoid

SUBMISSIONS_DIR = os.path.abspath("contests/submissions")

async def save_contest(name:str, submissions : dict[int:dict[nextcord.Attachment,str,str,float,int,int]]): # {submission_id:{"attachments":[],"text":"","avg":0,"sum":0,"count":0}}
    contest_info = {'contest name': name, 'submissions': [], 'date':datetime.now().date().isoformat()}
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
            filename =  f"file_{i}_{attachment.filename}"
            await attachment.save(os.path.join(save_dir,filename))
            submission_r["files"].append(filename)

        contest_info['submissions'].append(submission_r)

    print(os.path.abspath(f"{save_dir}/info.json"))
    with open(f"{save_dir}/info.json", "w") as info_file:
        info_file.write(json.dumps(contest_info, indent=4))

def get_all_contests():
    contests = []
    # Scan the submissions folder to find years and contests
    for year in os.listdir(SUBMISSIONS_DIR):
        year_path = os.path.join(SUBMISSIONS_DIR, year)
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
                            "submissions": contest_data.get("submissions", []),
                            "date": contest_data.get("date", datetime.min.date().isoformat())
                        })
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error reading {info_file}: {e}")

    contests.sort(key=lambda x: x["date"],reverse=True)

    return contests