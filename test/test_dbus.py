import sys
import os

import time

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from partyq.bluetooth.lbm import BluetoothBackend

client = BluetoothBackend()
client.start_scan()

print("starting scan sleeping for 10 seconds")
time.sleep(10)

client.stop_scan()

print(client.found_devices())

    