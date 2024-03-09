import os
from enum import Enum
import bleak


class DeviceType(Enum):
    LOCAL = auto()
    REMOTE = auto()


class Device:
    def __init__():
        platform = os.name
        source = DeviceType.LOCAL()

def list_remote_devices():
    pass
