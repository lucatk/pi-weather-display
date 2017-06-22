# -*- coding: utf-8 -*-
import sys
import threading

import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

import mainwindow_auto

import zmq
import json
import time
from datetime import datetime

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

def receive(form):

    zmqContext = zmq.Context()
    socket = zmqContext.socket(zmq.REP)
    socket.bind("tcp://127.0.0.1:5555")

    datastore = {
        "dht_temperature": [],
        "dht_humidity": [],
        "mcp_light_voltage": [],
        "mcp_smoke_voltage": []
    }

    while True:
        msg = socket.recv_json()
        data = json.loads(msg)

        datastore["dht_temperature"].insert(0, float(data["dht_temperature"]))
        if len(datastore["dht_temperature"]) > 60:
            datastore["dht_temperature"].pop()
        datastore["dht_humidity"].insert(0, float(data["dht_humidity"]))
        if len(datastore["dht_humidity"]) > 60:
            datastore["dht_humidity"].pop()
        datastore["mcp_light_voltage"].insert(0, float(data["mcp_light_voltage"]))
        if len(datastore["mcp_light_voltage"]) > 10:
            datastore["mcp_light_voltage"].pop()
        datastore["mcp_smoke_voltage"].insert(0, float(data["mcp_smoke_voltage"]))
        if len(datastore["mcp_smoke_voltage"]) > 60:
            datastore["mcp_smoke_voltage"].pop()

        socket.send_string("")

        sum = 0
        for val in datastore["dht_temperature"]:
            sum += val
        mittel = float(sum) / len(datastore["dht_temperature"])
        form.lblTemperature.setText(str(round(mittel, 1)).replace(".", ",") + "﻿°C")

        sum = 0
        for val in datastore["dht_humidity"]:
            sum += val
        mittel = float(sum) / len(datastore["dht_humidity"])
        form.lblHumidity.setText("Feuchtigkeit: " + str(round(mittel, 1)).replace(".", ",") + "%")

        sum = 0
        for val in datastore["mcp_light_voltage"]:
            sum += val
        mittel = float(sum) / len(datastore["mcp_light_voltage"])
        lightLevel = ((1-(float(mittel)/1023))/0.6)*100
        if lightLevel > 100:
            lightLevel = 100
        form.lblLightLevel.setText("Es ist " + str(round(lightLevel, 1)) + "% hell draußen.")

        sum = 0
        for val in datastore["mcp_smoke_voltage"]:
            sum += val
        mittel = float(sum) / len(datastore["mcp_smoke_voltage"])
        smokeLevel = (22000*3.3)/(float(mittel)/1023*3.3) - 22000
        form.lblSmokeLevel.setText("TGS2600: " + str(round(smokeLevel, 2)) + " Rs")

        form.lblTime.setText(datetime.now().strftime("%H:%M"))

def main():
    app = QApplication(sys.argv)
    app.setOverrideCursor(QtCore.Qt.BlankCursor)

    form = MainWindow()
    form.show()

    t = threading.Thread(target=receive, args=(form,))
    t.daemon = True
    t.start()
    # t.join()

    sys.exit(app.exec_())

if __name__ == "__main__":
  main()
