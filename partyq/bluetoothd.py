from partyq.device import DeviceManager
from partyq.logger import get_logger

logger = get_logger(__name__)

def start_scan(app):
    app["scand_event"].set()


def scand(app):
    logger.info("Starting bluetoothd")
    device_manager = app["DeviceManager"]
    triggered = app["scand_event"]
    while True:
        triggered.wait()
        logger.info("Starting scan")
        device_manager.list_devices()
        logger.info("Starting Event Loop Delegate")
        device_manager.run_delegate()
        logger.info("Exiting delegate loop")
        triggered.clear()

