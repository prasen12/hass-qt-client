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
Date Modified: Sat May 25 2024
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
    


