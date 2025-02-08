import sqlite3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

votes_table = """
CREATE TABLE IF NOT EXISTS votes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id VARCHAR(20) NOT NULL,
submission_id VARCHAR(20) NOT NULL,
rating INTEGER NOT NULL
)
 """

users_table = """
CREATE TABLE IF NOT EXISTS users (
user_id VARCHAR(20) PRIMARY KEY,
username VARCHAR(20),
last_update DATETIME NOT NULL
)
"""


def setup():
    conn = sqlite3.connect('data.db')
    conn.executescript(votes_table)
    conn.executescript(users_table)
    conn.commit()
    conn.close()

def run_query(query, params=None):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    if params is None:
        cursor.execute(query)
    else:
        cursor.execute(query, params)
    result = cursor.fetchall()
    conn.commit()
    conn.close()

    print(f"{query} {params} returned {len(result)} rows)")

    return result

