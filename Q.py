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

def peek() -> dict:
    if len(Q) > 0:
        return Q[0]
    return {}

def download(vid):
    buffer = BytesIO()
    yt = youtube.YTClient(vid)
    yt.get_best_audio_stream()
    yt.cur_stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer

def partyQ():
    logger.info("Starting PartyQ")
    while 1:
        meta = peek()
        vid = meta.get("videoId")
        if vid:
            # meta = db.get_metadata(vid)
            # meta = meta.pop(0)
            # db.update_playing(vid, True)
            logger.info("Playing %s", meta["title"])
            buffer = download(vid)
            logger.info("Downloaded %s", meta["title"])
            sound = AudioSegment.from_file(buffer)
            play(sound)
            # db.update_status(vid, "dequeue")
            # db.update_playing(vid, False)
            del sound
            del buffer
            gc.collect()
        time.sleep(1)
