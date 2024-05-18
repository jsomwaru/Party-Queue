from sdbus import DbusInterfaceCommon, dbus_method, dbus_property

BLUETOOTH_SERVICE_NAME = "org.bluez"

BLUETOOTH_INTERFACE_PATH = "/org/bluez/hci0"


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


class BluetoothManagerInterface(DbusInterfaceCommon,
                                interface_name="org.freedesktop.DBus.ObjectManager"):
    
    @dbus_method()
    def GetManagedObject():
        raise NotImplementedError

    

class BluetoothDiscoveryLinux(
    BluetoothDiscoveryInterface
):
    def __init__(self, bus):
        super().__init__()
        self.connect(BLUETOOTH_SERVICE_NAME, 
                     BLUETOOTH_INTERFACE_PATH, 
                     bus
        )


class BluetoothDeviceManager(
    BluetoothManagerInterface
):
    def __init__(self, bus):
        super().__init__()
        self.connect(BLUETOOTH_SERVICE_NAME, "/", bus)