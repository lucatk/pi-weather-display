# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btnTest = QtWidgets.QPushButton(self.centralWidget)
        self.btnTest.setGeometry(QtCore.QRect(260, 90, 231, 61))
        self.btnTest.setObjectName("btnTest")
        self.lblTest = QtWidgets.QLabel(self.centralWidget)
        self.lblTest.setGeometry(QtCore.QRect(345, 170, 60, 16))
        self.lblTest.setObjectName("lblTest")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnTest.setText(_translate("MainWindow", "Test Button"))
        self.lblTest.setText(_translate("MainWindow", "Hi!"))

