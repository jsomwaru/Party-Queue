class DeviceBackend:

    DEFAULT_SCAN_DURATION = 10

    def start_scan():
        raise NotImplementedError
    
    def stop_scan():
        raise NotImplementedError
    
    def found_devices():
        raise NotImplementedError