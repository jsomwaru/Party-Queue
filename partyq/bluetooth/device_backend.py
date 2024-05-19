class DeviceBackend:

    DEFAULT_SCAN_DURATION = 10

    def start_scan(self):
        raise NotImplementedError
    
    def stop_scan(self):
        raise NotImplementedError
    
    def found_devices(self):
        raise NotImplementedError
    
    def connect(self, device_id: str): 
        raise NotImplementedError
    
