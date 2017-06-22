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

    mode_temp = 0
    mode_clock = 0

    def changeTempMode(self, event):
        if self.mode_temp > 2:
            self.mode_temp = 0
        else:
            self.mode_temp = self.mode_temp+1

    def changeMCPMode(self, event):
        if self.mode_temp == 0:
            self.mode_temp = 1
        elif self.mode_temp == 1:
            self.mode_temp = 0
        elif self.mode_temp == 2:
            self.mode_temp = 3
        elif self.mode_temp == 3:
            self.mode_temp = 2

    def changeClockMode(self, event):
        if self.mode_temp == 0:
            self.mode_temp = 1
        else:
            self.mode_temp = 0

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()

        self.lblTemperature.mousePressEvent = self.changeTempMode
        self.lblHumidity.mousePressEvent = self.changeMCPMode
        self.lblLightLevel.mousePressEvent = self.changeMCPMode
        self.lblSmokeLevel.mousePressEvent = self.changeMCPMode
        self.lblTime.mousePressEvent = self.changeClockMode

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
        if form.mode_temp == 0:
            form.lblTemperature.setText(str(round(mittel, 1)).replace(".", ",") + "﻿°C")
        elif form.mode_temp == 1:
            form.lblTemperature.setText(str(round(mittel)) + "﻿°C")
        elif form.mode_temp == 2:
            mittel = (mittel * (9/5)) + 32
            form.lblTemperature.setText(str(round(mittel, 1)) + "﻿°F")
        elif form.mode_temp == 3:
            mittel = (mittel * (9/5)) + 32
            form.lblTemperature.setText(str(round(mittel)) + "﻿°F")


        sum = 0
        for val in datastore["dht_humidity"]:
            sum += val
        mittel = float(sum) / len(datastore["dht_humidity"])
        if form.mode_temp % 2 == 0:
            form.lblHumidity.setText("Feuchtigkeit: " + str(round(mittel, 1)).replace(".", ",") + "%")
        else:
            form.lblHumidity.setText("Feuchtigkeit: " + str(round(mittel)) + "%")

        sum = 0
        for val in datastore["mcp_light_voltage"]:
            sum += val
        mittel = float(sum) / len(datastore["mcp_light_voltage"])
        lightLevel = ((1-(float(mittel)/1023))/0.6)*100
        if lightLevel > 100:
            lightLevel = 100
        if form.mode_temp % 2 == 0:
            form.lblLightLevel.setText("Es ist " + str(round(lightLevel, 1)).replace(".", ",") + "% hell.")
        else:
            form.lblLightLevel.setText("Es ist " + str(round(lightLevel)) + "% hell.")

        sum = 0
        for val in datastore["mcp_smoke_voltage"]:
            sum += val
        mittel = float(sum) / len(datastore["mcp_smoke_voltage"])
        smokeLevel = (22000*3.3)/(float(mittel)/1023*3.3) - 22000
        if form.mode_temp % 2 == 0:
            form.lblSmokeLevel.setText("TGS2600: " + str(round(smokeLevel, 2)).replace(".", ",") + " Rs")
        else:
            form.lblSmokeLevel.setText("TGS2600: " + str(round(smokeLevel)) + " Rs")

        format = "%H:%M"
        if form.mode_clock == 1:
            format = "%I:%M%p"
        form.lblTime.setText(datetime.now().strftime(format))

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
