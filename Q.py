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

def enqueue(metadata):
    db.add_song(metadata)
    Q.append(metadata)


def dequeue():
    if len(Q) > 0:
        meta = Q.pop(0)
        vid = meta["videoId"]
        db.update_status(vid, "dequeue")
        db.update_playing(vid, False)
        return meta
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
            db.update_playing(vid, True)
            logger.info("Playing %s", meta["title"])
            buffer = download(vid)
            logger.info("Downloaded %s", meta["title"])
            sound = AudioSegment.from_file(buffer)
            play(sound)
            dequeue()
            del sound
            del buffer
            gc.collect()
        else:
            time.sleep(1)
