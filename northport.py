import threading
import serial
import time

baudrate_e = (9600,19200,38400,57600,115200)

class NorthPort:
    TX_MODE = 0
    RX_MODE = 1
    def __init__(self, com=None, baudrate=9600):
        self.mode = self.RX_MODE
        self.baudrate = 9600
        self.com = None
        self.port = None
        self.isActive = True
        self.rxCallback = None        
        self.setSerial(com,baudrate)
        self.rxThread = threading.Thread(target=self.rxProcess,daemon=False)
        self.rxThread.start()

    def setSerial(self,com=None,baudrate=9600):
        ports = self.getAvailablePorts()
        if baudrate_e.__contains__(baudrate) and (com in ports):
            self.com = com
            self.baudrate = baudrate
            self.port = serial.Serial(self.com,self.baudrate,timeout=1)

    def getAvailablePorts(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def receive(self):
        self.mode = self.RX_MODE
        try:
            if self.port == None: return
            if self.port.in_waiting > 0:
                return self.port.readline().decode('ascii')
        except serial.SerialException as e:
            pass

    def transmit(self, message):
        self.mode = self.TX_MODE
        try:
            self.port.write(message.encode())
        except AttributeError as e:
            print("Serial Not Found")
        self.mode = self.RX_MODE

    def rxProcess(self):
        #read data and callback when its ready
        while self.isActive:
            if self.mode == self.RX_MODE:
                self.rxData = self.receive()
                if self.rxData!=None and self.rxCallback!=None: 
                    self.rxCallback(self.rxData)

            time.sleep(0.01)
        
    def set_rxCallback(self,callback=None):
        self.rxCallback = callback

    def destroy(self):
        self.isActive = False
        if self.port != None:
            self.port.close()
