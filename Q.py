import gc
import time
import threading
from io import BytesIO

from pyaudio import PyAudio
from pydub.utils import make_chunks
from pydub import AudioSegment

import logger as log
import youtube

logger = log.get_logger(__name__)

CONTROL = threading.Event()

class QM:
    def __init__(self):
        self._q = []

    def enqueue(self, metadata):
        logger.debug("enqueue %s", str(metadata))
        metadata["pos"] = 0
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
    
    def time_callback(self, t):
        self.peek()["pos"] += (t / 1000)

    def remove(self, qpos):
        if qpos and qpos < len(self._q) and qpos > 0:
            del self._q[qpos]
    

def download(vid):
    buffer = BytesIO()
    yt = youtube.YTClient(vid)
    yt.get_best_audio_stream()
    yt.cur_stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer


def play_pyaudio(seg, time_callback):
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(seg.sample_width),
                    channels=seg.channels,
                    rate=seg.frame_rate,
                    output=True
                )
    try:
        CONTROL.set()
        duration = 500
        for frames in make_chunks(seg, duration):
            stream.write(frames._data)
            time_callback(duration)
            CONTROL.wait() # If not set thread will pause here
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


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
            play_pyaudio(sound, q.time_callback)
            q.dequeue()
            del sound
            del buffer
            gc.collect()
        else:
            time.sleep(1)
    logger.info("End of PartyQ")
