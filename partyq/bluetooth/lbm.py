import sdbus
from sdbus import DbusInterfaceCommon, dbus_method, dbus_property, DbusObjectManagerInterface

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


# class BluetoothManagerInterface(DbusInterfaceCommon,
#                                 interface_name="org.freedesktop.DBus.ObjectManager"):
    
#     @dbus_method()
#     def get_managed_objects():
#         raise NotImplementedError

    
class BluetoothDiscoveryLinux(
    BluetoothDiscoveryInterface
):
    def __init__(self, bus=None):
        super().__init__(
            BLUETOOTH_SERVICE_NAME, 
            BLUETOOTH_INTERFACE_PATH, 
            bus
        )
        # self.connect(BLUETOOTH_SERVICE_NAME, 
        #              BLUETOOTH_INTERFACE_PATH, 
        #              bus
        # )


# class BluetoothDeviceManager(
#     BluetoothManagerInterface
# ):
#     def __init__(self, bus=None):
#         super().__init__()
#         self.connect(BLUETOOTH_SERVICE_NAME, 
#                      BLUETOOTH_OBJECT_MANAGER_PATH, 
#                      bus
#         )


class BluetoothBackend(DeviceBackend):

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
        return self.device_manager.get_managed_objects()

