import gc
import time
from io import BytesIO

from pydub import AudioSegment
from pydub.playback import play

import logger as log
import youtube

logger = log.get_logger(__name__)

class QM:
    def __init__(self):
        self._q = []

    def enqueue(self, metadata):
        logger.info("enqueue %s", str(metadata))
        self._q.append(metadata)

    def dequeue(self):
        if len(self._q):
            return self._q.pop(0)
        return None
    
    def get_queue(self, filter=set()):
        if not len(filter):
            return self._q
        ret = []
        for v in self._q:
            entry = {}
            for k in filter:
                entry[k] = v.get(k)
            ret.append(entry)
        return ret
    
    def peek(self):
        if len(self._q):
            return self._q[0]
        return {}
    
    def get_by_videoid(self, vid):
        return [ entry for entry in self._q 
            if entry["videoId"] == vid
        ]
    

def download(vid):
    buffer = BytesIO()
    yt = youtube.YTClient(vid)
    yt.get_best_audio_stream()
    yt.cur_stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer


def partyQ(q: QM):
    logger.info("Starting PartyQ")
    while 1:
        meta = q.peek()
        vid = meta.get("videoId")
        if vid:
            logger.info("Playing %s", meta["title"])
            buffer = download(vid)
            logger.info("Downloaded %s", meta["title"])
            sound = AudioSegment.from_file(buffer)
            play(sound)
            q.dequeue()
            del sound
            del buffer
            gc.collect()
        else:
            time.sleep(1)
    logger.info("End of PartyQ")
