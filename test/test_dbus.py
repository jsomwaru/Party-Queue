import dbus
# for service in dbus.SystemBus().list_names():
#     print(service)

bus = dbus.SystemBus()

proxy = bus.get_object('org.bluez',
                       '/org/bluez/hci0')

print(proxy)