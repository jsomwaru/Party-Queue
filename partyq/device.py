import asyncio

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum, auto

import pyaudio
from bleak import BleakClient, BleakScanner

from partyq import logger as log

from partyq import config

logger = log.get_logger(__name__)


class DeviceType(str, Enum):
    REMOTE = auto()
    LOCAL = auto()

backend = config.get_device_backend()

class DeviceManager:
    """Manage Playback device
    """

    current_device = None
    remote_context = None
    last_refresh = None
    devices = set()
    
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
        self._backend = backend.BluetoothDeviceInquiryDelegate.alloc().init()
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

        
    async def set_playback_device(self, device :Device=None, device_id :str=None):
        if not device:
            device = await self.get_deivice_by_did(device_id)

        if self.remote_context:
            await self.disconnect()

        if not device:
            return False
        elif device.dtype == DeviceType.REMOTE:
            DeviceManager.current_device = device
            DeviceManager.remote_context = BleakClient(device.did)
            await DeviceManager.remote_context.connect()
            return True
        elif device.dtype == DeviceType.LOCAL:
            DeviceManager.current_device = device
            DeviceManager.remote_context = None
            return True

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
        if config.PLATFORM == "darwin": 
            ret["devices"] =  [ 
                {
                    "dtype": DeviceType.REMOTE, 
                    "did": d._.addressString, 
                    "name": d._.name
                } 
                for d in self._backend.found_devices() 
            ]
            logger.info(ret)
        elif config.PLATFORM == "linux":
            ret["devices"] = [ 
                {
                    "dtype": DeviceType.REMOTE, 
                    "did": d['org.bluez.Device1']["Address"][1], 
                    "name": d['org.bluez.Device1']["Name"][1] 
                } 
                for d in self._backend.found_devices() 
            ]
        return ret
    
    def run_delegate(self):
        """Used to execute event loop or handle timeouts in native environments
        """
        backend.run()
