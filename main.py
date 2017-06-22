import sys

import PyQt5
from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import *

import mainwindow_auto

from threading import Thread
import time

import Adafruit_DHT

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()

sensor_DHT = Adafruit_DHT.DHT22
sensor_DHT_PIN = 4

dht_temp = 0
dht_humidity = 0

def sensors():
    global dht_temp
    global dht_humidity
    while True:
        humid, temp = Adafruit_DHT.read(sensor_DHT, sensor_DHT_PIN)
        if humid is not None:
            dht_humidity = humid
        if temp is not None:
            dht_temp = temp
        time.sleep(1)

def main():
    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()

    sensorThread = Thread(target=sensors)
    sensorThread.start()
    sensorThread.join()

    while True:
        print(dht_temp)
        print(dht_humidity)

    sys.exit(app.exec_())

if __name__ == "__main__":
  main()
