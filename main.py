
#pyrcc5.exe .\resource.qrc -o .\resource_rc.py
#pyuic5.exe .\northstar.ui -o .\northstar_ui.py

import sys
import serial
import serial.tools.list_ports
import threading
from northport import *

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction
from PyQt5.QtCore import Qt, pyqtSlot, QFile, QTextStream
from northstar_ui import Ui_MainWindow

class Northstar(QMainWindow):
    def __init__(self):
        super(Northstar,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.w_page.setCurrentIndex(0)
        self.ui.send.clicked.connect(self.send)
        self.ui.sendmsg.returnPressed.connect(self.send)

        self.ui.menuSerial.aboutToShow.connect(self.portSearch)
        self.ui.action9600.triggered.connect(lambda: self.setBaudRate(9600))
        self.ui.action19200.triggered.connect(lambda: self.setBaudRate(19200))
        self.ui.action38400.triggered.connect(lambda: self.setBaudRate(38400))
        self.ui.action57600.triggered.connect(lambda: self.setBaudRate(57600))
        self.ui.action115200.triggered.connect(lambda: self.setBaudRate(115200))
        
        self.serial_port = NorthPort()
        
    def setComPort(self, port):
        self.ui.comportLabel.setText(port)
        self.serial_port.setComPort(port)

    def setBaudRate(self,baud):
        self.ui.baudrateLabel.setText(str(baud))
        self.serial_port.setComPort(baud)

        self.serial_thread = threading.Thread(target=self.portProcess)
        self.serial_thread.start()

    def send(self):
        message = self.ui.sendmsg.text()
        self.serial_port.transmit(message)

        self.ui.console.insertPlainText(message+"\r\n")
        self.ui.sendmsg.clear()
        self.ui.sendmsg.setFocus()
        self.ui.console.verticalScrollBar().setValue(self.ui.console.verticalScrollBar().maximum())

    def portSearch(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.ui.menuCOM.clear()
        for port in ports:
            act = QAction(port, self)
            act.text = port
            act.triggered.connect(lambda:self.setComPort(port))
            self.ui.menuCOM.addAction(act)
            print(port + " added.")


    def portProcess(self):
        while self.serial_port.port.is_open:
            message = self.serial_port.readline()
            if message:
                self.ui.console.insertPlainText(message)
                self.ui.console.verticalScrollBar().setValue(self.ui.console.verticalScrollBar().maximum())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("style.qss","r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = Northstar()
    window.show()

    sys.exit(app.exec())