import time
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

import db
import youtube

Q = []

def enqueue(metadata):
    Q.append(metadata["videoId"])
    conn = db.setup_db()
    db.add_song(conn, metadata)

def dequeue():
    if len(Q) > 0:
        return Q.pop(0)
    return None

def download(vid):
    buffer = BytesIO()
    yt = youtube.YTClient(vid)
    yt.get_best_audio_stream()
    yt.cur_stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer

def partyQ():
    print("starting partyq")
    while 1:
        vid = dequeue()
        if vid:
            print(f"playing {vid}")
            buffer = download(vid)
            print("downloaded")
            sound = AudioSegment.from_file(buffer)
            play(sound)
        time.sleep(1)
