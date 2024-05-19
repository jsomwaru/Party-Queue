import sdbus
from sdbus import DbusInterfaceCommon, dbus_method, dbus_property, DbusObjectManagerInterface

from partyq.bluetooth.device_backend import DeviceBackend

import re

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


class BluetoothDiscoveryLinux(
    BluetoothDiscoveryInterface
):
    def __init__(self, bus=None):
        super().__init__(
            BLUETOOTH_SERVICE_NAME, 
            BLUETOOTH_INTERFACE_PATH, 
            bus
        )


class BluetoothBackend(DeviceBackend):

    pairable_device_filter = re.compile(r"/org/bluez/hci0/dev_.*")

    def __init__(self):
        super().__init__()
        sdbus.set_default_bus(sdbus.sd_bus_open_system())
        self.discovery = BluetoothDiscoveryLinux()   
        self.device_manager = DbusObjectManagerInterface(BLUETOOTH_SERVICE_NAME, BLUETOOTH_OBJECT_MANAGER_PATH)

    def start_scan(self):
        self.discovery.start_discovery()

    def stop_scan(self):
        self.discovery.stop_discovery()

    def found_devices(self):
        return self._parse_devices(
            self.device_manager.get_managed_objects()
        )
    
    def connect(self, device_id: str):
        self.discovery.register_player([device_id])
    
    def _parse_devices(self, found_devices: dict):
        devices = {}
        for device, meta in found_devices.items():
            if re.match(self.pairable_device_filter, device):
                devices[device] = meta
        return devices 

    