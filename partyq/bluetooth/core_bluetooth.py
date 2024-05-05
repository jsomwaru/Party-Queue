import logging

import objc
from CoreBluetooth import (CBUUID, CBCentralManager, CBManagerStatePoweredOff,
                           CBManagerStatePoweredOn, CBManagerStateResetting,
                           CBManagerStateUnauthorized, CBManagerStateUnknown,
                           CBManagerStateUnsupported, CBConnectionEventMatchingOptionServiceUUIDs,  CBConnectPeripheralOptionNotifyOnConnectionKey)
from Foundation import NSObject, NSMutableDictionary, NSArray
from libdispatch import DISPATCH_QUEUE_SERIAL, dispatch_queue_create

from bleak.uuids import normalize_uuid_16, uuid16_dict

logging.basicConfig()
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

CBCentralManagerDelegate = objc.protocolNamed("CBCentralManagerDelegate")

UUIDS = {
    0x1108: "Headset",
    0x1109: "Cordless Telephony",
    0x110A: "Audio Source",
    0x110B: "Audio Sink",
}

class CentralManagerDelegate(NSObject):

    ___pyobjc_protocols__ = [CBCentralManagerDelegate]

    def init(self):
        self = objc.super(CentralManagerDelegate, self).init()


        self.central_manager = CBCentralManager.alloc().initWithDelegate_queue_(
            self, dispatch_queue_create(b"partyq.corebluetooth", DISPATCH_QUEUE_SERIAL)
        )

        self.callbacks = {}
        return self
    

    @objc.python_method
    def start_scan(self):
        logger.debug("starting scan")

        self.central_manager.scanForPeripheralsWithServices_options_(
            None, None
        )


    @objc.python_method
    def did_discover_peripheral(self, central_manager, peripheral, advertisement_data, rssi):
        logging.debug("discovered")
        for i in self.callbacks.values():
            i(central_manager, peripheral, advertisement_data)


    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, central: CBCentralManager, peripheral, advertisementData, RSSI):
        logger.debug("centralManager_didDiscoverPeripheral_advertisementData_RSSI_")
        self.did_discover_peripheral(
            central,
            peripheral,
            advertisementData,
            RSSI
        )

    def centralManager_connectionEventDidOccur_forPeripheral_(self, *args):
        logger.debug("connection event occured")


    def centralManagerDidUpdateState_(self, centralManager: CBCentralManager) -> None:
        logger.debug("centralManagerDidUpdateState_")
        if centralManager.state() == CBManagerStateUnknown:
            logger.debug("Cannot detect bluetooth device")
        elif centralManager.state() == CBManagerStateResetting:
            logger.debug("Bluetooth is resetting")
        elif centralManager.state() == CBManagerStateUnsupported:
            logger.debug("Bluetooth is unsupported")
        elif centralManager.state() == CBManagerStateUnauthorized:
            logger.debug("Bluetooth is unauthorized")
        elif centralManager.state() == CBManagerStatePoweredOff:
            logger.debug("Bluetooth powered off")
        elif centralManager.state() == CBManagerStatePoweredOn:
            logger.debug("Bluetooth powered on")
            d = NSMutableDictionary.dictionary()
            uuids = [normalize_uuid_16(u) for u in uuid16_dict.keys()]
            services = NSArray.alloc().initWithArray_(
                list(map(CBUUID.UUIDWithString_, uuids))
            )
            # audio_service = CBUUID.UUIDWithString_(normalize_uuid_16(0x110B))
            # logger.debug(CBConnectionEventMatchingOption)
            # logger.debug("services %s", services)
            d[CBConnectionEventMatchingOptionServiceUUIDs] = services
            d[CBConnectPeripheralOptionNotifyOnConnectionKey] = True
            centralManager.registerForConnectionEventsWithOptions_(d)
            logger.debug("central manager scanning -- %s", a.central_manager.isScanning())
            self.start_scan()
            


if __name__ == "__main__":
    import time
    
    a = CentralManagerDelegate.alloc().init()
    a.callbacks[id(a)] = lambda x,y,z : print(x, y, z)
    time.sleep(10)
    