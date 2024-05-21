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

Created Date: Saturday, Apr 6th 2024, 11:06:10 am

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from ha_qt_client.homeassistant_client.areas import Area
import random

class RoomsPanel(QtWidgets.QFrame):
    room_selected = QtCore.pyqtSignal(str)
    
    def __init__(self, parent: QtWidgets.QWidget=None) -> None:
        super().__init__(parent)
   
        self.setObjectName("RoomsPanel")
        self.resize(640, 480)
        uic.loadUi('qtdesigns/rooms_panel.ui', self)
        self.__gridLayoutWidget = self.findChild(QtWidgets.QWidget, 'gridLayoutWidget')
        self.__gridLayout =  self.findChild(QtWidgets.QGridLayout, 'gridLayout')
        self.__refButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        # Remove this from the layout widget as this only for reference to create similar buttons
        self.__refButton.setParent(None)
        
    def add_rooms(self, rooms:list[Area]) -> None:
        row = 0 
        col = 0
        maxCols = 1 if len(rooms) <=3 else 3
        for room in sorted(rooms, key=(lambda x: x.name)):
            button = QtWidgets.QPushButton(self.__gridLayoutWidget)
            button.setSizePolicy(self.__refButton.sizePolicy())
            button.setObjectName(room.area_id)
            button.setText(room.name)
            button.setFont(self.__refButton.font())
            button.clicked.connect(self.on_room_selected)
            button.setStyleSheet(self.__refButton.styleSheet())
            self.__gridLayout.addWidget(button, row, col, 1, 1)
            if (col < maxCols-1):
                col = col + 1
            else:
                col = 0
                row = row + 1

    def on_room_selected(self):
        self.room_selected.emit(self.sender().objectName())
        