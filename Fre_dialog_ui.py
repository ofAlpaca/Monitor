# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Fre_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Frequence_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(200, 150))
        Dialog.setMaximumSize(QtCore.QSize(200, 150))
        self.text_freq = QtWidgets.QLineEdit(Dialog)
        self.text_freq.setGeometry(QtCore.QRect(140, 40, 41, 20))
        self.text_freq.setObjectName("text_freq")
        self.label_freq = QtWidgets.QLabel(Dialog)
        self.label_freq.setGeometry(QtCore.QRect(20, 40, 121, 16))
        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_freq.setFont(font)
        self.label_freq.setObjectName("label_freq")
        self.btn_submit = QtWidgets.QPushButton(Dialog)
        self.btn_submit.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.btn_submit.setObjectName("btn_submit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_freq.setText(_translate("Dialog", "Slave Frequence : "))
        self.btn_submit.setText(_translate("Dialog", "Submit"))

