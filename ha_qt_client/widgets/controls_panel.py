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

Created Date: Saturday, Apr 13th 2024, 11:34:48 am

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''


from PyQt5 import uic, QtWidgets


class ControlsPanel(QtWidgets.QFrame):
    
    def __init__(self, parent:QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.__setupUi()
        
    def __setupUi(self):
        uic.loadUi('qtdesigns/controls_panel.ui', self)
    
    def setRoomName(self, name:str):
        label = self.findChild(QtWidgets.QLabel, 'label_header_text')
        if label:
            label.setText(name)

    def on_shades_button_clicked(self, fn):
        button = self.findChild(QtWidgets.QPushButton, 'push_button_shades')
        button.clicked.connect(fn)
    
    def on_rooms_button_clicked(self, fn):
        button = self.findChild(QtWidgets.QPushButton, 'push_button_rooms')
        button.clicked.connect(fn)
    