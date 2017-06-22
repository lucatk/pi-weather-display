import sys

import PyQt5
from PyQt5.QtWidgets import *

import mainwindow_auto

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(PyQt5.QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint)

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    qdw = PyQt5.QtGui.QDesktopWidget()
    screen = qdw.screenGeometry(screen=1)
    form.centralWidget.setGeometry(screen)
    sys.exit(app.exec_())

if __name__ == "__main__":
  main()
