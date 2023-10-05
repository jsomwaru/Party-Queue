import sqlite3

def setup_db():
    db = sqlite3.connect("media/q.db")
    db.execute(
        "CREATE TABLE IF NOT EXISTS Q(videoId PRIMARY KEY, name, requestor, status)"
    )
    return db

def add_song(conn, metadata):
    conn.execute(
        "INSERT INTO Q VALUES (?,?,?,?)", metadata["videoId"], 
        metadata["name"], metadata["requestor"], "playing"
    )

def update_status(conn, video_id, status):
    conn.execute(
        "UPDATE Q SET status = ? WHERE videoId=?", video_id, status
    )