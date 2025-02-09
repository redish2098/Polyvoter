import json
import os
from datetime import datetime
import nextcord
import nanoid

SUBMISSIONS_DIR = "contests/submissions"

async def save_contest(name:str, submissions : dict[int:dict[nextcord.Attachment,str,float,int,int]]): # {submission_id:{"attachments":[],"text":"","avg":0,"sum":0,"count":0}}
    contest_info = {'contest name': name, 'submissions': []}
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

