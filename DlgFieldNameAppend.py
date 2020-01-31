# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgFieldNameAppend.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgFieldNameAppend(object):
    def setupUi(self, dlgFieldNameAppend):
        dlgFieldNameAppend.setObjectName("dlgFieldNameAppend")
        dlgFieldNameAppend.resize(187, 79)
        self.line = QtWidgets.QFrame(dlgFieldNameAppend)
        self.line.setGeometry(QtCore.QRect(10, 38, 167, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(dlgFieldNameAppend)
        self.label.setGeometry(QtCore.QRect(14, 12, 63, 16))
        self.label.setObjectName("label")
        self.etFieldName = QtWidgets.QTextEdit(dlgFieldNameAppend)
        self.etFieldName.setGeometry(QtCore.QRect(72, 8, 104, 25))
        self.etFieldName.setObjectName("etFieldName")
        self.btOk = QtWidgets.QPushButton(dlgFieldNameAppend)
        self.btOk.setGeometry(QtCore.QRect(102, 50, 75, 23))
        self.btOk.setObjectName("btOk")

        self.retranslateUi(dlgFieldNameAppend)
        QtCore.QMetaObject.connectSlotsByName(dlgFieldNameAppend)

    def retranslateUi(self, dlgFieldNameAppend):
        _translate = QtCore.QCoreApplication.translate
        dlgFieldNameAppend.setWindowTitle(_translate("dlgFieldNameAppend", "Append field"))
        self.label.setText(_translate("dlgFieldNameAppend", "Fieldname"))
        self.btOk.setText(_translate("dlgFieldNameAppend", "Ok"))
