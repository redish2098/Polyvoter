from bot.database import schema
from bot import settings
import numpy as np

def new_contest():
    schema.run_query("DELETE FROM votes WHERE TRUE")

def get_votes(n : int = 10) -> dict[int, tuple[float,int,int]]: # {submission_id:(avg,sum,count)}
    user_averages = schema.run_query("SELECT user_id, AVG(rating) as avg_rating FROM votes GROUP BY user_id")

    avg_ratings = np.array([row[1] for row in user_averages])
    mean = np.mean(avg_ratings)
    std_dev = np.std(avg_ratings)

    z_threshold = 2
    valid_users = {row[0] for row in user_averages if abs(row[1] - mean) <= z_threshold * std_dev}

    if valid_users:
        placeholders = ",".join("?" * len(valid_users))
        query = f"""
            SELECT submission_id, 
                AVG(rating) as avg_votes, 
                SUM(rating) as sum_votes,
                COUNT(rating) as count_votes
            FROM votes 
            WHERE user_id IN ({placeholders}) 
            GROUP BY submission_id
            ORDER BY avg_votes DESC
            Limit {n}
        """
        valid_votes = schema.run_query(query, tuple(valid_users))
    else:
        valid_votes = []

    return {x[0]:(x[1],x[2],x[3]) for x in valid_votes}

def clear_votes():
    schema.run_query("DELETE FROM votes WHERE TRUE")

def set_vote(user_id : int, submission_id : int ,score: int) -> None:
    schema.run_query("DELETE FROM votes WHERE user_id = ? AND submission_id = ?", (user_id, submission_id))
    schema.run_query("INSERT INTO votes (user_id, submission_id, rating) VALUES (?, ?, ?)", (user_id, submission_id, score))

def remove_vote(user_id : int, submission_id : int, value : int) -> None:
    schema.run_query("DELETE FROM votes WHERE user_id = ? AND submission_id = ? AND rating = ?", (user_id, submission_id, value))

def delete_submission_votes(submission_id : int) -> None:
    schema.run_query("DELETE FROM votes WHERE submission_id = ?", (submission_id,))

def delete_user_votes(user_id : int) -> None:
    schema.run_query("DELETE FROM votes WHERE user_id = ?", (user_id,))
