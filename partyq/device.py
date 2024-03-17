import asyncio

from dataclasses import dataclass, asdict
from enum import Enum, auto

import pyaudio
from bleak import BleakClient, BleakScanner

from partyq import logger as log

logger = log.get_logger(__name__)


class DeviceType(str, Enum):
    REMOTE = auto()
    LOCAL = auto()

class DeviceManager:
    """Manage Playback device
    """

    current_device = None
    remote_context = None
    
    @dataclass
    class Device:
        dtype: DeviceType
        did: str 
        name: str
        def __eq__(self, other): return self.did == other.did and self.dtype == other.dtype
        def __hash__(self): return hash((self.dtype, self.did, self.name))

    def __init__(self):
        self.devices = set()
        self._audio = pyaudio.PyAudio()

    async def _local_devices(self):
        info = self._audio.get_host_api_info_by_index(0)
        device_count = info.get("deviceCount")
        for i in range(device_count):
            if self._audio.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels') > 0:
                self.devices.add(self.Device(
                    DeviceType.LOCAL, str(i), self._audio.get_device_info_by_host_api_device_index(0, i).get("name")))

    async def _remote_devices(self):
        devices = await BleakScanner.discover()
        for d in devices:
            self.devices.add(self.Device(DeviceType.REMOTE, d.name, d.address))
    
    async def set_playback_device(self, device: Device):
        if device.dtype == DeviceType.REMOTE:
            self.current_device = device
            self.remote_context = await BleakClient(device.did).connect()
        elif device.dtype == DeviceType.LOCAL:
            self.current_device = device
            self.remote_context = None

    async def disconnect(self):
        if self.current_device and self.current_device.dtype == DeviceType.REMOTE:
            try:
                self.remote_context.disconnect()
            except Exception:
                logger.exception("Encountered error while disconnecting")
                return False
        return True
    
    async def list_devices(self):
        await asyncio.gather(self._remote_devices(),  self._local_devices())
        return self.device_dict()
    

    def device_dict(self):
        return {
            "devices": [asdict(d) for d in self.devices]
        }
