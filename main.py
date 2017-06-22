# -*- coding: utf-8 -*-
import sys
import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

import mainwindow_auto

import zmq
import json
import time

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()

        bgPalette = self.centralWidget.palette()
        bgPalette.setColor(self.centralWidget.backgroundRole(), QtCore.Qt.black)
        self.centralWidget.setPalette(bgPalette)

def main():
    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()

    zmqContext = zmq.Context()
    socket = zmqContext.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    while True:
        data = json.loads(socket.recv_json())

        form.lblTemperature.setText(str(round(data["dht_temperature"])) + "﻿°C")
        form.lblHumidity.setText("Feuchtigkeit".join([str(round(data["dht_humidity"])), "%"]))

        socket.send("")

    sys.exit(app.exec_())

if __name__ == "__main__":
  main()
