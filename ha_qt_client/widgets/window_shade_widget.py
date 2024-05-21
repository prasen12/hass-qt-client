'''
MIT License

Copyright (c) 2024 Prasen Palvankar

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

Created Date: Tuesday, Mar 26th 2024, 6:26:37 pm

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''

from collections.abc import Callable
from typing_extensions import Self
from PyQt5 import QtWidgets, uic, QtCore, QtGui

class WindowShadeWidget(QtWidgets.QFrame):
    
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('qtdesigns/blind_control_widget.ui', self)
        self.__vertical_slider_percent_open = self.findChild(QtWidgets.QSlider, 'verticalslider_percent_open')
        self.__button_open = self.findChild(QtWidgets.QPushButton, 'button_open')
        self.__button_close = self.findChild(QtWidgets.QPushButton, 'button_close')
        self.__label_percent_open = self.findChild(QtWidgets.QLabel, 'label_percent_open')
        self.__label_name = self.findChild(QtWidgets.QLabel, 'label_name')

        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        # self.setSizePolicy(size_policy)
        # self.setMinimumSize(QtCore.QSize(180, 180))
        # self.setMaximumSize(QtCore.QSize(150, 150))
        # self.setStyleSheet("background-color: rgb(126, 82, 247);")
        # self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.setFrameShadow(QtWidgets.QFrame.Raised)
        
        # vertical_layout_widget = QtWidgets.QWidget(self)
        # vertical_layout_widget.setGeometry(QtCore.QRect(10, 10, 161, 161))
        # vertical_layout_widget.setObjectName("vertical_layout_widget")
        # vertical_layout_2 = QtWidgets.QVBoxLayout(vertical_layout_widget)
        # vertical_layout_2.setContentsMargins(0, 0, 0, 0)
        # vertical_layout_2.setObjectName("vertical_layout_2")
        
        # self.__label_name = QtWidgets.QLabel(vertical_layout_widget)
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setBold(True)
        # vertical_layout_2.addWidget(self.__label_name)
        # self.__label_name.setFont(font)
        # self.__label_name.setStyleSheet("color: rgb(255, 255, 255);")
        # self.__label_name.setAlignment(QtCore.Qt.AlignCenter)
        # self.__label_name.setObjectName("label_name")
        
        # widget_main_container = QtWidgets.QWidget(vertical_layout_widget)
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(widget_main_container.sizePolicy().hasHeightForWidth())
        # widget_main_container.setSizePolicy(size_policy)
        # widget_main_container.setObjectName("widget_main_container")
        # horizontal_layout_widget_2 = QtWidgets.QWidget(widget_main_container)
        # horizontal_layout_widget_2.setGeometry(QtCore.QRect(0, 0, 151, 141))
        # horizontal_layout_widget_2.setObjectName("horizontal_layout_widget_2")
        # hbox_layout_main = QtWidgets.QHBoxLayout(horizontal_layout_widget_2)
        # hbox_layout_main.setContentsMargins(0, 0, 0, 0)
        # hbox_layout_main.setSpacing(1)
        # hbox_layout_main.setObjectName("hbox_layout_main")
        
        # widget_slider_container = QtWidgets.QWidget(horizontal_layout_widget_2)
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # size_policy.setHorizontalStretch(1)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(widget_slider_container.sizePolicy().hasHeightForWidth())
        # widget_slider_container.setSizePolicy(size_policy)
        # widget_slider_container.setMinimumSize(QtCore.QSize(50, 0))
        # widget_slider_container.setObjectName("widget_slider_container")
        # self.__label_percent_open = QtWidgets.QLabel(widget_slider_container)
        # self.__label_percent_open.setGeometry(QtCore.QRect(0, 110, 51, 20))
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setBold(True)
        # self.__label_percent_open.setFont(font)
        # self.__label_percent_open.setStyleSheet("color: rgb(255, 255, 255);")
        # self.__label_percent_open.setAlignment(QtCore.Qt.AlignCenter)
        # self.__label_percent_open.setObjectName("labelPercentOpen")
        # self.__vertical_slider_percent_open = QtWidgets.QSlider(widget_slider_container)
        # self.__vertical_slider_percent_open.setGeometry(QtCore.QRect(10, 0, 31, 111))
        # self.__vertical_slider_percent_open.setOrientation(QtCore.Qt.Vertical)
        # self.__vertical_slider_percent_open.setObjectName("vertical_slider_percent_open")
        # self.__vertical_slider_percent_open.setInvertedAppearance(True)
        # hbox_layout_main.addWidget(widget_slider_container)
        
        # widget_buttons = QtWidgets.QWidget(horizontal_layout_widget_2)
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # size_policy.setHorizontalStretch(2)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(widget_buttons.sizePolicy().hasHeightForWidth())
        # widget_buttons.setSizePolicy(size_policy)
        # widget_buttons.setObjectName("widget_buttons")
        # layout_widget = QtWidgets.QWidget(widget_buttons)
        # layout_widget.setGeometry(QtCore.QRect(1, 0, 95, 131))
        # layout_widget.setObjectName("layout_widget")
        
        # vertical_layout_buttons = QtWidgets.QVBoxLayout(layout_widget)
        # vertical_layout_buttons.setContentsMargins(0, 0, 0, 0)
        # vertical_layout_buttons.setSpacing(10)
        # vertical_layout_buttons.setObjectName("vertical_layout_buttons")
        
        # self.__button_close = QtWidgets.QPushButton(layout_widget)
        # self.__button_close.setText('Close')
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(self.__button_close.sizePolicy().hasHeightForWidth())
        # self.__button_close.setSizePolicy(size_policy)
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setBold(True)
        # self.__button_close.setFont(font)
        # self.__button_close.setStyleSheet("background-color: rgb(255, 149, 66);")
        # self.__button_close.setObjectName("buttonClose")
        # vertical_layout_buttons.addWidget(self.__button_close)
        
        # self.__button_open = QtWidgets.QPushButton(layout_widget)
        # self.__button_open.setText('Open')
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(self.__button_open.sizePolicy().hasHeightForWidth())
        # self.__button_open.setSizePolicy(size_policy)
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setBold(True)
        # self.__button_open.setFont(font)
        # self.__button_open.setStyleSheet("background-color: rgb(112, 199, 138);")
        # self.__button_open.setObjectName("button_open")
        # vertical_layout_buttons.addWidget(self.__button_open)
        
        # hbox_layout_main.addWidget(widget_buttons)
        # vertical_layout_2.addWidget(widget_main_container)


    
    def on_slider_position_changed(self, fn:Callable[[int, Self]]):
        self.__vertical_slider_percent_open.valueChanged.connect(lambda x: fn(100-x, self))
    
    def on_open_clicked(self, fn:Callable[[Self]]):
        self.__button_open.clicked.connect(lambda x: fn(self))
    
    def on_close_clicked(self, fn:Callable[[Self]]):
        self.__button_close.clicked.connect(lambda x: fn(self))
    
    @property
    def slider_position(self):
        return 100-(self.__vertical_slider_percent_open.sliderPosition())

    @slider_position.setter
    def slider_position(self, coverPosition:int):
        if coverPosition is not None:
            self.__vertical_slider_percent_open.setSliderPosition(100-coverPosition)
            if coverPosition == 100:
                self.__label_percent_open.setText('Open')
            elif coverPosition == 0:
                self.__label_percent_open.setText('Closed')
            else:
                self.__label_percent_open.setNum(coverPosition)
    
    @property 
    def name(self):
        return self.__label_name.text() 
    @name.setter
    def name(self, s:str):
        self.__label_name.setText(s)
    
    @property
    def entity_id(self):
        return self.__entity_id
    
    @entity_id.setter
    def entity_id(self, id:str):
        self.__entity_id = id
    


