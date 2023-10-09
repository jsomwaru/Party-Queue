import sqlite3


def get_cursor() -> sqlite3.Cursor:
    db = sqlite3.connect("media/q.db")
    cur = db.cursor()
    return cur

def setup_db():
    db = sqlite3.connect("media/q.db")

    db.execute(
        "CREATE TABLE IF NOT EXISTS Q(videoId, songName, requestor, status)"
    )
    print("table created")
    db.commit()
    db.close()

def add_song(metadata):
    db = sqlite3.connect("media/q.db")
    db.execute(
        "INSERT INTO Q VALUES (?,?,?,?)", 
        (metadata["videoId"], metadata["title"], metadata["requestor"],"enqueue")
    )
    print("addedd song to db")
    db.commit()
    db.close()

def update_status(video_id, status):
    db = sqlite3.connect("media/q.db")
    db.execute(
        "UPDATE Q set status = ? WHERE videoId = ?", (status, video_id ))
    db.commit()
    db.close()

def get_by_status(status):
    cur, = get_cursor()
    res = cur.execute("SELECT * FROM Q WHERE status = ?", status)
    return format_results(res.fetchall())

def format_results(results):
    return [{
            "videoId": res[0],
            "songName": res[1],
            "requestor": res[2],
            "status": res[3]
        } 
        for res in results if len(res) == 4
    ]