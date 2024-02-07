import threading
import serial
import time

baudrate_e = (9600,19200,38400,57600,115200)

class NorthPort:
    NO_CONNECTION = -1
    TX_MODE = 0
    RX_MODE = 1
    def __init__(self, com=None, baudrate=9600):
        self.mode = self.NO_CONNECTION
        self.baudrate = 9600
        self.com = None
        self.port = None
        self.isActive = True

        self.portErrorCallback = None
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
            self.mode = self.RX_MODE

    def getAvailablePorts(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def receive(self):
        try:
            if self.port == None: return
            if self.port.in_waiting > 0:
                try:
                    return self.port.readline().decode("ascii")
                except UnicodeDecodeError as a:
                    return None
        except serial.SerialException as e:
            self.mode = self.NO_CONNECTION
            if self.portErrorCallback != None:
                self.portErrorCallback()
            print("Serial Not Found")
            return None

    def transmit(self, message):
        if (self.port == None or self.mode==self.NO_CONNECTION):
            return
        self.mode = self.TX_MODE
        self.port.write(message.encode())
        self.mode = self.RX_MODE

    def rxProcess(self):
        #read data and callback when its ready
        while self.isActive:
            if self.mode == self.RX_MODE:
                self.rxData = self.receive()
                if self.rxData!=None and self.rxCallback!=None: 
                    self.rxCallback(self.rxData)

            time.sleep(0.01)
        
    def destroy(self):
        self.isActive = False
        if self.port != None:
            self.port.close()
