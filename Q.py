import gc
import time
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

import db
import logger as log
import youtube

Q = []

logger = log.get_logger(__name__)

def enqueue(videoId):
    Q.append(videoId)

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
            meta = db.get_metadata(vid)
            meta = meta.pop(0)
            db.update_playing(vid, True)
            logger.info("Playing %s", meta["songName"])
            buffer = download(vid)
            logger.info("Downloaded %s", meta["songName"])
            sound = AudioSegment.from_file(buffer)
            play(sound)
            db.update_status(vid, "dequeue")
            db.update_playing(vid, False)
            del sound
            del buffer
            gc.collect()
        time.sleep(1)
