import sqlite3


def get_db() -> sqlite3.Cursor:
    db = sqlite3.connect("media/q.db")
    return db

def setup_db():
    db = sqlite3.connect("media/q.db")
    db.execute(
        "CREATE TABLE IF NOT EXISTS Q(videoId, songName, requestor, status, playing)"
    )
    print("table created")
    db.commit()
    db.close()

def add_song(metadata):
    db = sqlite3.connect("media/q.db")
    db.execute(
        "INSERT INTO Q VALUES (?,?,?,?,?)", 
        (metadata["videoId"], metadata["title"], metadata["requestor"], "enqueue", False)
    )
    print("addedd song to db")
    db.commit()
    db.close()

def update_status(video_id, status):
    db = sqlite3.connect("media/q.db")
    db.execute(
        "UPDATE Q set status = ? WHERE videoId = ?", (status, video_id))
    db.commit()
    db.close()

def update_playing(video_id, playing):
    db = sqlite3.connect("media/q.db")
    db.execute(
        "UPDATE Q set playing = ? WHERE videoId = ?", (playing, video_id))
    db.commit()
    db.close()

def get_by_status(status):
    db = get_db()
    res = db.execute("SELECT * FROM Q WHERE status = ?", [status])
    return format_results(res.fetchall())

def get_metadata(vid):
    db = get_db()
    res = db.execute("SELECT * from Q WHERE videoId = ?", [vid])
    return format_results(res.fetchall())

def format_results(results):
    if len(results) > 0:
        return [{
                "videoId": res[0],
                "songName": res[1],
                "requestor": res[2],
                "status": res[3],
                "playing": res[4]
            } 
            for res in results if len(res) == 5
        ]
    return []
    