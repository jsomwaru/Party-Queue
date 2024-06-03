import re
import time

import sdbus
from sdbus import (DbusInterfaceCommon, DbusObjectManagerInterface,
                   dbus_method)

from partyq.bluetooth.device_backend import DeviceBackend

BLUETOOTH_SERVICE_NAME = "org.bluez"

BLUETOOTH_INTERFACE_PATH = "/org/bluez/hci0"

BLUETOOTH_OBJECT_MANAGER_PATH = "/"


class BluetoothDiscoveryInterface(DbusInterfaceCommon,
                                  interface_name='org.bluez.Adapter1'):

    @dbus_method()
    def start_discovery(self):
        raise NotImplementedError

    @dbus_method()
    def stop_discovery(self):
        raise NotImplementedError

    @dbus_method("oa{sv}")
    def register_player(self, player: list):
        raise NotImplementedError


class BluetoothDeviceInterface(DbusInterfaceCommon,
                               interface_name="org.bluez.Device1"):
    @dbus_method()
    def connect():
        raise NotImplementedError

    @dbus_method()
    def pair():
        raise NotImplementedError

    @dbus_method()
    def disconnect():
        raise NotImplementedError


# DbusObjectManagerInterface is provided by sdbus
class BluetoothDiscoveryLinux(
    BluetoothDiscoveryInterface
):
    def __init__(self, bus=None):
        super().__init__(
            BLUETOOTH_SERVICE_NAME,
            BLUETOOTH_INTERFACE_PATH,
            bus
        )


class BluetoothDevice(BluetoothDeviceInterface):
    def __init__(self, device_path: str, bus=None):
        super().__init__(
            BLUETOOTH_SERVICE_NAME,
            device_path,
            bus
        )

class BluetoothBackend(DeviceBackend):

    pairable_device_filter = re.compile(r"/org/bluez/hci0/dev_.*")

    def __init__(self):
        super().__init__()
        sdbus.set_default_bus(sdbus.sd_bus_open_system())
        bus = sdbus.sd_bus_open_system()
        self.discovery = BluetoothDiscoveryLinux(bus)
        self.device_manager = DbusObjectManagerInterface(BLUETOOTH_SERVICE_NAME,
                                                         BLUETOOTH_OBJECT_MANAGER_PATH, bus)

    def start_scan(self):
        self.discovery.start_discovery()

    def stop_scan(self):
        self.discovery.stop_discovery()

    def found_devices(self):
        return self._parse_devices(
            self.device_manager.get_managed_objects()
        )

    def connect(self, device_id: str) -> BluetoothDevice:
        bus = sdbus.sd_bus_open_system()
        device_path = self.get_deivce_path_by_id(device_id)
        device = BluetoothDevice(device_path, bus)
        device.connect()
        return device

    def get_device_path_by_id(self, device_id: str):
        for device_path, meta in self.found_devices().items():
            if meta['org.bluez.Device1']["Address"][1] == device_id:
                return device_path


    def _parse_devices(self, found_devices: dict):
        devices = {}
        for device, meta in found_devices.items():
            if re.match(self.pairable_device_filter, device):
                devices[device] = meta
        return devices

def new_backend():
    return BluetoothBackend()


def run():
    time.sleep(BluetoothBackend.DEFAULT_SCAN_DURATION)
