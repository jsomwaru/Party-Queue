import os 
from dasbus.connection import SessionMessageBus
os.environ["DISPLAY"] = ":0.0"
bus = SessionMessageBus()
b = bus.get_proxy('org.bluez', '/org/bluez/hci0')
dir(b)
