import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import sqlite3
import db


metadata = {
    "title": "test-song",
    "videoId": "1",
    "requestor": "me",
    "status": "enqueue"
}

db.add_song(metadata)

# conn = sqlite3.connect("../media/q.db")

# # db.update_status("1", "playing")

# cur = conn.execute("SELECT * FROM Q WHERE 1=1")

# print(cur.fetchall())

# conn.close()