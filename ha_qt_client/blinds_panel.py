'''
MIT License

Copyright (c) 2024 Oracle

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created Date: Tuesday, Mar 19th 2024, 10:11:02 pm

Author: Prasen Palvankar

----
Date Modified: Mon Mar 25 2024
Modified By: Prasen Palvankar
----
'''
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QSize
from blinds_panel_frame import Ui_BlindsPanel
from entity import Entity

class BlindsPanel(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget, roomName:str) -> None:
        super().__init__(parent)
        self.__setupUi(roomName)
        self.__coverEntitySliders = dict()

    def __setupUi(self, roomName):
        self.setObjectName('BlindsView')
        self.resize(640, 480)
        self.setMinimumSize(QSize(640, 480))
        self.setMaximumSize(QSize(640, 480))
        layoutWidget = QtWidgets.QWidget(self)
        layoutWidget.setGeometry(QRect(0, 0, 641, 481))
        layoutWidget.setObjectName("layoutWidget")
        self.__verticalLayout = QtWidgets.QVBoxLayout(layoutWidget)
        self.__verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.__verticalLayout.setSpacing(0)
        self.__verticalLayout.setObjectName("self.__verticalLayout")
        headerFrame = QtWidgets.QFrame(layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(headerFrame.sizePolicy().hasHeightForWidth())
        headerFrame.setSizePolicy(sizePolicy)
        headerFrame.setMaximumSize(QSize(640, 40))
        headerFrame.setAutoFillBackground(False)
        headerFrame.setStyleSheet("background-color: rgb(154, 242, 176);")
        headerFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        headerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        headerFrame.setObjectName("headerFrame")
        layoutWidget1 = QtWidgets.QWidget(headerFrame)
        layoutWidget1.setGeometry(QRect(0, 0, 641, 46))
        layoutWidget1.setObjectName("layoutWidget1")
        headerHorizontalLayout = QtWidgets.QHBoxLayout(layoutWidget1)
        headerHorizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        headerHorizontalLayout.setContentsMargins(0, 1, 5, 6)
        headerHorizontalLayout.setSpacing(2)
        headerHorizontalLayout.setObjectName("headerHorizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(120, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        headerHorizontalLayout.addItem(spacerItem)
        headerLabel = QtWidgets.QLabel(layoutWidget1)
        headerLabel.setStyleSheet("font: 28pt;\n"
"background-color: rgb(154, 242, 176);")
        headerLabel.setAlignment(Qt.AlignCenter)
        headerLabel.setObjectName("headerLabel")
        headerLabel.setText(f'{roomName} Blinds')
        headerHorizontalLayout.addWidget(headerLabel)
        self.__backButton = QtWidgets.QPushButton(layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.__backButton.sizePolicy().hasHeightForWidth())
        self.__backButton.setSizePolicy(sizePolicy)
        self.__backButton.setMinimumSize(QSize(120, 34))
        self.__backButton.setMaximumSize(QSize(120, 34))
        self.__backButton.setStyleSheet("background-color: rgb(89, 135, 91);\n"
"color: rgb(247, 247, 247);")
        self.__backButton.setObjectName("backButton")
        headerHorizontalLayout.addWidget(self.__backButton)
        self.__verticalLayout.addWidget(headerFrame)
        self.mainContainerFrame = QtWidgets.QFrame(layoutWidget)
        self.mainContainerFrame.setStyleSheet("background-color: rgb(175, 172, 255);")
        self.mainContainerFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainContainerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainContainerFrame.setObjectName("mainContainerFrame")
        self.__gridLayoutWidget = QtWidgets.QWidget(self.mainContainerFrame)
        self.__gridLayoutWidget.setGeometry(QRect(-10, 0, 651, 441))
        self.__gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.blindsControlsGridLayout = QtWidgets.QGridLayout(self.__gridLayoutWidget)
        self.blindsControlsGridLayout.setContentsMargins(0, 0, 0, 0)
        self.blindsControlsGridLayout.setHorizontalSpacing(6)
        self.blindsControlsGridLayout.setObjectName("blindsControlsGridLayout")
    
    def onBackButtonClicked(self, fn):
        self.__backButtonClickedHandler = fn
    
    def onCloseAllBlinds(self, fn):
        self.__closeAllBlindsHandler = fn
    
    def onOpenAllBlinds(self, fn):
        self.__openAllBlindsHandler = fn
    
    def onBlindPositionChanged(self, fn):
        self.__blindPositionChangedHandler = fn
    
    def setCurrentPosition(self, coverEntities:list[Entity]):
        for coverEntity in coverEntities:
            verticalSlider:QtWidgets.QSlider = self.__coverEntitySliders.get(coverEntity.entityId)
            verticalSlider.setSliderPosition(100-coverEntity.currentPosition)
    
    def onCloseButtonClicked(self, fn):
        self.__closeButtonClickedHandler = fn
    
    def onOpenButtonClicked(self, fn):
        self.__openButtonClickedHandler = fn

    
    def addBlind(self, coverEntity: Entity, row: int, col: int):
        blindContolFrame = QtWidgets.QFrame(self.__gridLayoutWidget)
        blindContolFrame.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(blindContolFrame.sizePolicy().hasHeightForWidth())
        blindContolFrame.setSizePolicy(sizePolicy)
        blindContolFrame.setMinimumSize(QSize(150, 120))
        blindContolFrame.setMaximumSize(QSize(150, 120))
        blindContolFrame.setStyleSheet("background-color: rgb(121, 82, 255);\n"
"color: rgb(245, 241, 246);")
        blindContolFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        blindContolFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        blindContolFrame.setObjectName("blindContolFrame")
        
        verticalSlider = QtWidgets.QSlider(blindContolFrame)
        verticalSlider.setGeometry(QRect(10, 30, 41, 71))
        verticalSlider.setMaximum(100)
        verticalSlider.setProperty("value", 100)
        verticalSlider.setSliderPosition(100-coverEntity.currentPosition)
        verticalSlider.setOrientation(Qt.Vertical)
        verticalSlider.setInvertedAppearance(True)
        verticalSlider.setObjectName("verticalSlider")
        verticalSlider.valueChanged.connect(lambda x: labelPercentOpen.setNum(abs(x-100)))
        
        
        closeButton = QtWidgets.QPushButton(blindContolFrame)
        closeButton.setGeometry(QRect(60, 30, 80, 41))
        closeButton.setStyleSheet("background-color: rgb(255, 87, 112);")
        closeButton.setObjectName("closeButton")
        closeButton.setText('Close')
        
        openButton = QtWidgets.QPushButton(blindContolFrame)
        openButton.setGeometry(QRect(60, 70, 80, 41))
        openButton.setStyleSheet("background-color: rgb(115, 196, 144);")
        openButton.setObjectName("openButton")
        openButton.setText('Open')
        
        label = QtWidgets.QLabel(blindContolFrame)
        label.setGeometry(QRect(10, 10, 131, 10))
        label.setMinimumSize(QSize(0, 10))
        label.setMaximumSize(QSize(16777215, 10))
        label.setStyleSheet("font: 12pt ;")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("label")
        label.setText(coverEntity.name)
        
        labelPercentOpen = QtWidgets.QLabel(blindContolFrame)
        labelPercentOpen.setGeometry(QRect(10, 100, 41, 16))
        labelPercentOpen.setAlignment(Qt.AlignCenter)
        labelPercentOpen.setObjectName("labelPercentOpen")
        labelPercentOpen.setNum(coverEntity.currentPosition)
        
        self.blindsControlsGridLayout.addWidget(blindContolFrame, row, col, 1, 1)
        
        self.__verticalLayout.addWidget(self.mainContainerFrame)
        self.__coverEntitySliders[coverEntity.entityId] = verticalSlider


