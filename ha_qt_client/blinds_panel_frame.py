# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'blinds_panel_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BlindsPanel(object):
    def setupUi(self, BlindsPanel):
        BlindsPanel.setObjectName("BlindsPanel")
        BlindsPanel.resize(626, 480)
        self.gridLayoutWidget = QtWidgets.QWidget(BlindsPanel)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 591, 451))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.retranslateUi(BlindsPanel)
        QtCore.QMetaObject.connectSlotsByName(BlindsPanel)

    def retranslateUi(self, BlindsPanel):
        _translate = QtCore.QCoreApplication.translate
        BlindsPanel.setWindowTitle(_translate("BlindsPanel", "Blinds"))
