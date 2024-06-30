import asyncio

from dataclasses import dataclass, asdict
from enum import Enum, auto

import pyaudio

from partyq import logger as log

from partyq.config import AppConfig

import re

logger = log.get_logger(__name__)


class DeviceType(str, Enum):
    REMOTE = auto()
    LOCAL = auto()

backend = AppConfig.get_device_backend()

class DeviceManager:
    """Manage Playback device
    """

    current_device = None
    remote_context = None
    last_refresh = None
    devices = None

    local_device_id = re.compile("$\d^")

    @dataclass
    class Device:
        dtype: DeviceType
        did: str
        name: str
        def __eq__(self, other): return self.did == other.did and self.dtype == other.dtype
        def __hash__(self): return hash((self.dtype, self.did, self.name))
        def asdict(self): return asdict(self)

    def __init__(self):
        self._audio = pyaudio.PyAudio()
        self._backend = backend.new_backend()
        self.device_queue = asyncio.Queue()
        self.event = asyncio.Event()

    def _local_devices(self):
        info = self._audio.get_host_api_info_by_index(0)
        device_count = info.get("deviceCount")
        local_devices = set()
        for i in range(device_count):
            if self._audio.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels') > 0:
                local_devices.add(self.Device(
                    DeviceType.LOCAL, str(i), self._audio.get_device_info_by_host_api_device_index(0, i).get("name")))
        return local_devices

    def _remote_devices(self):
        self._backend.start_scan()


    async def set_playback_device(self, device_id :str=None):

        if not device_id:
            return False
        elif not re.match(self.local_device_id, device_id):
            DeviceManager.current_device = device_id
            self._backend.connect(device_id)
            return True
        else:
            logger.info("Local device not implemented")

    async def disconnect(self):
        if self.current_device and self.current_device.dtype == DeviceType.REMOTE:
            try:
                await DeviceManager.remote_context.disconnect()
            except Exception:
                logger.exception("Encountered error while disconnecting")
                return False
        return True

    def list_devices(self):
        self._remote_devices()
        return True

    def get_devices(self):
        """BAD
        This help retrieve devices from the scanning backend
        """
        ret = { }
        if AppConfig.PLATFORM == "darwin":
            ret["devices"] =  [
                {
                    "dtype": DeviceType.REMOTE,
                    "did": d._.addressString,
                    "name": d._.name
                }
                for d in self._backend.found_devices()
            ]
            logger.info(ret)
        elif AppConfig.PLATFORM == "linux":
            ret["devices"] = [
                {
                    "dtype": DeviceType.REMOTE,
                    "did": d['org.bluez.Device1']["Address"][1],
                    "name": d['org.bluez.Device1']["Name"][1] if "Name" in d['org.bluez.Device1'] else d['org.bluez.Device1']["Alias"][1]
                }
                for d in self._backend.found_devices().values()
            ]
        return ret

    def run_delegate(self,duration=10):
        """Used to execute event loop or handle timeouts in native environments
        """
        backend.run(duration=duration)

    def cancel(self):
        self._backend.stop_scan()
