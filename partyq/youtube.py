import os
from io import BytesIO

import ytmusicapi

from pytube import YouTube

from partyq import logger as log 

logger = log.get_logger(__name__)

DATA_DIR="media"
BROWSER_FILE = os.path.join(DATA_DIR, "browser.json")

class NoStreamFoundException(Exception):
    pass

async def search(query):
    ytm = None
    if os.path.exists(BROWSER_FILE):
        logger.info("Found YouTube Music Auth File")
        ytm = ytmusicapi.YTMusic(BROWSER_FILE)
    else:
        logger.info("Upload YouTube Music auth file to manage library")
        ytm = ytmusicapi.YTMusic()
    results = ytm.search(query, filter="songs")
    return results

class YTClient:
    """
    Looper wrapper around pytube for downloading audio streams
    """

    base_url = "https://www.youtube.com/watch?v={}"

    def __init__(self, video_id):
        url = self.base_url.format(video_id)
        self.yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        self._stream = None

    def get_best_audio_stream(self, best_effort=True):
        """
        @param best_effort: by default enabled - extract from video if not able to find audio stream
        """
        if not self.is_audio_available and not best_effort:
            raise NoStreamFoundException("Audio stream not found")
        self._stream = self.yt.streams.get_audio_only()

    @property
    def streams(self):
        return self.yt.streams

    @property
    def is_audio_available(self):
        return self.streams.get_audio_only() is not None

    def streams_to_json(self):
        return self.yt.metadata

    def download_stream(self, buffer: BytesIO):
        self.cur_stream.stream_to_buffer(buffer)
        buffer.seek(0)

    @property
    def cur_stream(self):
        if self._stream is None:
            self.get_best_audio_stream()
        return self._stream

    def metadata(self):
        return {
            "title": self.cur_stream.title,
            "duration": None,
            "format": self.cur_stream.mime_type,
            "abr": self.cur_stream.abr,
            "filesize": self.cur_stream.filesize
        }

