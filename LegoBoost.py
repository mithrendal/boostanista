import cb
import sound
import struct

class MyCentralManagerDelegate (object):
    def __init__(self):
        self.peripheral = None

    def did_discover_peripheral(self, p):
        print('+++ Discovered peripheral: %s (%s)' % (p.name, p.uuid))
        if p.name and 'LEGO' in p.name and not self.peripheral:
            # Keep a reference to the peripheral, so it doesn't get garbage-collected:
            self.peripheral = p
            cb.connect_peripheral(self.peripheral)

    def did_connect_peripheral(self, p):
        print('*** Connected: %s' % p.name)
        print('Discovering services...')
        p.discover_services()

    def did_fail_to_connect_peripheral(self, p, error):
        print('Failed to connect')

    def did_disconnect_peripheral(self, p, error):
        print('Disconnected, error: %s' % (error,))
        self.peripheral = None

    def did_discover_services(self, p, error):
        for s in p.services:
            print('found service %s' % s.uuid)
            p.discover_characteristics(s)

    def did_discover_characteristics(self, s, error):
        print('did_discover_characteristics for service:'+ s.uuid)
        
        for c in s.characteristics:
            print('characteristic='+ c.uuid)
            
            print('write to led lamp...')
            self.peripheral.write_characteristic_value(c, b'\x08\x00\x81\x32\x11\x51\x00\x06', True)

    def did_write_value(self, c, error):
        print('response from device: did write value')

    def did_update_value(self, c, error):
        print('did_update_value '+ c.uuid);
        print('Button value: %s' % c.value.encode('hex'))
        sound.play_effect('Beep')
    

delegate = MyCentralManagerDelegate()
print('Scanning for peripherals...')
cb.set_central_delegate(delegate)
cb.scan_for_peripherals()

# Keep the connection alive until the 'Stop' button is pressed:
try:
    while True: pass
except KeyboardInterrupt:
    # Disconnect everything:
    cb.reset()
