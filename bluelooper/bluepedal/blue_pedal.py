import struct
import time
from bluepy import btle

class BluePedal (btle.DefaultDelegate):

    __HNDL_BUTTON0 = 0x0e
    __HNDL_BUTTON1 = 0x11
    __HNDL_LED0 = 0x15
    __HNDL_LED1 = 0x17
    PRESSED = 1
    RELEASED = 2
    RELEASED_LONG = 3
    LED_OFF = 1
    LED_ON = 2
    LED_BLINKING = 3

    def __init__(self,pedal_name):
        btle.DefaultDelegate.__init__(self)
        self.button_callback = None
        self.pedal_name = pedal_name
        self.p = None

    def connect(self):
        while True:
            address = self.__scan()
            if address != None:
                break
            else:
                print("[BluePedal: pedal not found, trying again")
                time.sleep(0.1)

        if address != None:
            return self.__connect(address)
        else:
            return None

    def waitForNotifications(self, timeout = 1):
        if self.p != None:
            return self.p.waitForNotifications(timeout);
        return False


    def __scan(self):
        scanner = btle.Scanner(0)
        devices = scanner.scan(5.0)
        address = None

        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Complete Local Name":
                    if value.startswith(self.pedal_name):
                        address = dev
                        print("[BluePedal] found pedal at %s" % dev.addr)
                        return address
        return None

    def __connect(self,address):
        self.p = btle.Peripheral( address )
        self.p.setDelegate( self )

        # activate notifications
        self.p.writeCharacteristic(self.__HNDL_BUTTON0+1, struct.pack('<bb', 0x01, 0x00),withResponse=False )
        self.p.writeCharacteristic(self.__HNDL_BUTTON1+1, struct.pack('<bb', 0x01, 0x00),withResponse=False )
        print("[BluePedal] connected")


    def handleNotification(self, cHandle, data):
        # find button ID
        if cHandle == self.__HNDL_BUTTON0:
            button_id = 0;
        elif cHandle == self.__HNDL_BUTTON1:
            button_id = 1;

        #find button state
        state = struct.unpack('B',data)[0]

        if self.button_callback != None:
            self.button_callback(button_id, state)

    def setLEDState(self, ledID, state):
        if ledID == 0:
            handle = self.__HNDL_LED0
        elif ledID == 1:
            handle = self.__HNDL_LED1
        else:
            raise IndexError('[BLUE_PEDAL] setLEDState: Invalid LED index')

        if state == self.LED_OFF:
            value = struct.pack('<b',0x01)
        elif state == self.LED_ON:
            value = struct.pack('<b',0x02)
        elif state == self.LED_BLINKING:
            value = struct.pack('<b',0x03)
        else:
            raise ValueError('[BLUE_PEDAL] setLEDState: Invalid LED state value')
        self.p.writeCharacteristic(handle,value ,withResponse=False )
