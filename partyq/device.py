import asyncio

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
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
        self.device_queue = asyncio.Queue()
        self.event = asyncio.Event()

    async def _local_devices(self):
        info = self._audio.get_host_api_info_by_index(0)
        device_count = info.get("deviceCount")
        local_devices = set()
        for i in range(device_count):
            if self._audio.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels') > 0:
                local_devices.add(self.Device(
                    DeviceType.LOCAL, str(i), self._audio.get_device_info_by_host_api_device_index(0, i).get("name")))
        return local_devices

    async def _remote_devices(self):
        devices = await BleakScanner.discover(return_adv=True, cb=dict(use_bdaddr=True))
        print(devices)
        remote_devices = set()
        for did, device in devices.items():
            d, adv = device
            print(did, adv)
            print(d.address, d.name)
            remote_devices.add(self.Device(DeviceType.REMOTE, d.address, d.name))
        return remote_devices
    
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
            # await DeviceManager.remote_context.get_services()
            # print(DeviceManager.remote_context.services)
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
    
    async def list_devices(self):
        results = await asyncio.gather(self._remote_devices(),  self._local_devices())
        DeviceManager.devices = set.union(*results)
        DeviceManager.last_refresh = datetime.now(tz=timezone.utc)
        return self.device_dict()
    

    async def get_devices(self, cb):
        while True:
            device = await self.device_queue.get()
            resp = await cb(device)
            if resp == False:
                self.scan_task.cancel()
                break
        return
    
    
    async def list_devices_streaming(self, event: asyncio.Event):
        async def scan():
            async with BleakScanner(self._device_detection_callback):
                await event.wait()
        self.scan_task = asyncio.create_task(scan())


    async def _device_detection_callback(self, device, adv_data):
        logger.info(f"Discovered Device {device}")
        device = self.Device(DeviceType.REMOTE, device.address, device.name)
        await self.device_queue.put(device)

    def device_dict(self):
        return {
            "devices": [d.asdict() for d in self.devices]
        }

    async def get_deivice_by_did(self, did):
        for d in DeviceManager.devices:
            if d.did == did:
                return d
        return None
