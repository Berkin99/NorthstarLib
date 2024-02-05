
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSlot, QFile, QTextStream

from northstar_ui import Ui_MainWindow

#pyrcc5.exe .\resource.qrc -o .\resource_rc.py
#pyuic5.exe .\northstar.ui -o .\northstar_ui.py

class Northstar(QMainWindow):
    def __init__(self):
        super(Northstar,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.w_page.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("style.qss","r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = Northstar()
    window.show()

    sys.exit(app.exec())