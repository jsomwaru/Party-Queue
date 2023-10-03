from io import BytesIO

import time

import youtube

from pydub import AudioSegment
from pydub.playback import play


Q = []

def enqueue(video_id):
    Q.append(video_id)

def dequeue():
    if len(Q) > 0:
        return Q.pop(0)
    return None

def download(vid):
    yt = youtube.YTClient(vid)
    yt.get_best_audio_stream()
    buffer = BytesIO()
    yt.cur_stream.stream_to_buffer(buffer)
    return buffer

def partyQ():
    print("starting partyq")
    while 1:
        vid = dequeue()
        if vid:
            print(f"playing {vid}")
            buffer = download(vid)
            buffer.seek(0)
            sound = AudioSegment.from_file(buffer)
            play(sound)
        time.sleep(1)
