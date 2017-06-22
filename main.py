import sys
import PyQt5
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import *

import mainwindow_auto

import zmq
import time

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()

        bgPalette = self.centralWidget.palette()
        bgPalette.setColor(self.centralWidget.backgroundRole(), Qt.black)
        self.centralWidget().setPalette(bgPalette)

def main():
    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()



    sys.exit(app.exec_())

if __name__ == "__main__":
  main()
