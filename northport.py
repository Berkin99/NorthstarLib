
import serial

baudrate_e = (9600,19200,38400,57600,115200)

class NorthPort():
    com = None
    baudrate = 115200

    def __init__(self, com=None, baud=115200):
        self.com = com
        if baudrate_e.__contains__(baud):
            self.baudrate = baud
            if com!=None:    
                self.port = serial.Serial(self.com,self.baudrate,timeout=1)

    def setBaudRate(self, baud):
        if baudrate_e.__contains__(baud):
            self.baudrate = baud
            self.port = serial.Serial(self.com,self.baudrate,timeout=1)

    def setComPort(self, com):
        self.port = com
        self.port = serial.Serial(self.com,self.baudrate,timeout=1)
    
    def readline(self):
        try:
            self.rx_data = self.port.readline().decode("ascii")
            return self.rx_data;
        except serial.SerialException as e:
            return False

    def transmit(self, message):
        try:
            self.serial_port.write(message.encode())
        except AttributeError as e:
            print("Serial Not Found")