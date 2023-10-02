from io import BytesIO

import pyaudio

import youtube

from pydub import AudioSegment
from pydub.playback import play

from pyogg import OpusDecoder

Q = []

def enqueue(video_id):
    Q.append(video_id)
    print(Q)

def dequeue():
    if len(Q) > 0:
        return Q.pop(0)
    return None


def partyQ():
    CHUNK = 1000
    p = pyaudio.PyAudio()
    print("starting partyq")
    opus_decoder = OpusDecoder()
    opus_decoder.set_channels(2)
    opus_decoder.set_sampling_frequency(48000)
    while 1:
        vid = dequeue()
        if vid:
            print(f"playing {vid}")
            yt = youtube.YTClient(vid)
            yt.get_best_audio_stream()
            buffer = BytesIO()
            yt.cur_stream.stream_to_buffer(buffer)
         
            buffer.seek(0)
            sound = AudioSegment.from_file(buffer)
            play(sound)

