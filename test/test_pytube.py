import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from youtube import YTClient

VID = "Bn-lcvrMOlc"

video = YTClient(VID)

video.get_best_audio_stream()

print(video.streams)
