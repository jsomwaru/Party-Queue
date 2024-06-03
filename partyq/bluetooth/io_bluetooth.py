import time

import IOBluetooth
import objc
from AppKit import NSAnyEventMask, NSApplication, NSApplicationDefined
from Foundation import NSDate, NSDefaultRunLoopMode
from IOBluetooth import IOBluetoothDeviceInquiry, IOBluetoothDevicePair

from partyq.bluetooth.device_backend import DeviceBackend
from partyq.logger import get_logger

logger = get_logger(__name__)

IOBluetoothDeviceInquiryDelegate = objc.protocolNamed("IOBluetoothDeviceInquiryDelegate")
IOBluetoothDevicePairDelegate = objc.protocolNamed("IOBluetoothDevicePairDelegate")


class BluetoothDeviceInquiryDelegate(IOBluetooth.NSObject):

    ___pyobjc_protocols__ = [IOBluetoothDeviceInquiryDelegate]

    def init(self):
        self = objc.super(BluetoothDeviceInquiryDelegate, self).init()
        self.client = IOBluetoothDeviceInquiry.inquiryWithDelegate_(self)
        return self

    @objc.python_method
    def start_scan(self):
        print("starting scan")
        self.client.start()
    
    @objc.python_method
    def stop_scan(self):
        self.client.stop()

    @objc.python_method
    def found_devices(self):
        return self.client.foundDevices()

    def deviceInquiryDeviceFound_(self, *args):
        print(args)

    def deviceInquiryStarted_(self, arg):
        logger.info("Inquiry started")

    def deviceInquiryUpdatingDeviceNamesStarted_devicesRemaining_(self, a, b):
        logger.error("deviceInquiryUpdatingDeviceNamesStarted_devicesRemaining_: %s, %s", a, b)

    def deviceInquiryComplete_error_aborted_(self, inquiry, err, aborted):
        logger.error("Encountered error %s during %s aborted %s", err, inquiry, aborted)
        return

class BluetoothDevicePair(IOBluetooth.NSObject):
    __pyobjc_protocols__ = [IOBluetoothDevicePairDelegate]
    def init(self):
        self = objc.super(BluetoothDevicePair, self).init()
        self.client = IOBluetoothDevicePair.alloc().init()
        self.client.setDelegate_(self)
        return self
    
    @objc.python_method
    def device(self):
        return self.client.device()
    
    @objc.python_method
    def set_device(self, device):
        self.client.setDevice_(device)

    @objc.python_method
    def start(self):
        self.client.start()

    @objc.python_method
    def stop(self): 
        self.client.stop()


class BluetoothBackend(DeviceBackend):

    def __init__(self):
        self.discovery = BluetoothDeviceInquiryDelegate.alloc().init()
        self.device_manager = BluetoothDevicePair.alloc().init()

    def start_scan(self):
        self.discovery.start_scan()

    def stop_scan(self):
        self.discovery.stop_scan()

    def connect(self, device_id):
        device = None
        logger.info("Device Cache %s", self.found_devices())
        for d in self.found_devices():
            if d._.addressString == device_id:
                logger.info("device found")
                self.device_manager.set_device(device)
                status_code = self.device_manager.start()
                logger.info("device pairing starting status code: %s", status_code)
                run()
                self.device_manager.stop()
                run(duration=1)
                break
        else:
            logger.info("Device %s not found in %d devices", device_id, len(self.found_devices()))
            return 

    def found_devices(self):
        return self.discovery.found_devices()

def new_backend():
    return BluetoothBackend()


def run(duration=10):
    app = NSApplication.sharedApplication()
    start = time.time()
    timeout = start + duration
    logger.info("Starting NSApplication")
    while True:
        cur_time = time.time()
        if cur_time > timeout:
                break
        try:
            e = app.nextEventMatchingMask_untilDate_inMode_dequeue_(NSAnyEventMask, NSDate.dateWithTimeIntervalSinceNow_(timeout - cur_time), NSDefaultRunLoopMode, True)
        except Exception as e:
            print("failed starting app")
            print(e)
            exit(555)
        if e is not None:
            if (e.type() == NSApplicationDefined):
                print(e)
                return True    
            else:
                app.postEvent_atStart_(e, True)
    logger.info("Exiting NSApplication Event loop")


# inquiry = IOBluetoothDeviceInquiry.inquiryWithDelegate_(delegate)
# inquiry = IOBluetoothDeviceInquiry.alloc().init()

# inquiry.setDelegate_(delegate)

# inquiry.updateNewDeviceNames()

# delegate = BluetoothDeviceInquiryDelegate.alloc().init()
# delegate.start_scan()
# run()
# print(delegate.client.foundDevices())


# delegate.start_scan()

# time.sleep(10)




