import IOBluetooth
from IOBluetooth import IOBluetoothDeviceInquiry, IOBluetoothDevicePair
from Foundation import NSDefaultRunLoopMode, NSDate 

from AppKit import NSApplication, NSAnyEventMask, NSApplicationDefined

import time

import objc

from partyq.bluetooth.device_backend import DeviceBackend

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
        # self.discovered(arg)
        print("inquiry started")

    def deviceInquiryUpdatingDeviceNamesStarted_devicesRemaining_(self, a, b):
        print("deviceInquiryUpdatingDeviceNamesStarted_devicesRemaining_")

    def deviceInquiryComplete_error_aborted_(self, inquiry, err, abortedQ):
        print("error")

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

    def connect(self, device):
        self.device_manager.set_device(device)
        self.device_manager.start()
        run()
        self.device_manager.stop()

    def found_devices(self):
        return self.discovery.found_devices()

def new_backend():
    return BluetoothBackend()


def run(duration=10):
     app = NSApplication.sharedApplication()
     start = time.time()
     timeout = start + duration
     print("NSapplication", app)
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
        else:
            print(e)


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




