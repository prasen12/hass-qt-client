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

Created Date: Tuesday, Mar 26th 2024, 6:52:22 pm

Author: Prasen Palvankar

----
Date Modified: Sat May 25 2024
Modified By: Prasen Palvankar
----
'''

from PyQt5 import QtWidgets, uic

from ha_qt_client.widgets import window_shade_widget
from collections.abc import Callable

class WindowShadesPanel(QtWidgets.QFrame):
    
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        
        self.__window_shade_widgets:dict[str, window_shade_widget.WindowShadeWidget] = dict()
        self.resize(640, 480)
        uic.loadUi('qtdesigns/blinds_panel.ui', self)
        
        self.__label_header = self.findChild(QtWidgets.QLabel, 'label_headerText')
        self.__grid_layout_main = self.findChild(QtWidgets.QGridLayout, 'gridLayout_blindsWidget')
        self.__button_back = self.findChild(QtWidgets.QPushButton, 'pushButton_back')
        self.__button_close_all = self.findChild(QtWidgets.QPushButton, 'pushButton_closeAll')
        self.__button_open_all = self.findChild(QtWidgets.QPushButton, 'pushButton_openAll')
        
    @property
    def header_text(self):
        return self.__label_header.text()
    
    @header_text.setter
    def header_text(self, s:str):
        self.__label_header.setText(s)
        
    def add_window_shade_widget(self, widget:window_shade_widget.WindowShadeWidget, row:int, col:int):
        self.__grid_layout_main.addWidget(widget, row, col, 1, 1)
        self.__window_shade_widgets[widget.entity_id] = widget
        
    def get_window_shade_widget(self, entity_id:str):
        return self.__window_shade_widgets.get(entity_id)

    def on_back_clicked(self, fn:Callable):
        self.__button_back.clicked.connect(fn)
        
    def on_close_all_clicked(self, fn:Callable[[list[window_shade_widget.WindowShadeWidget]]]):
        self.__button_close_all.clicked.connect(lambda x: fn(list(self.__window_shade_widgets.values())))
    
    def on_open_all_clicked(self, fn:Callable[[list[window_shade_widget.WindowShadeWidget]]]):
        self.__button_open_all.clicked.connect(lambda x: fn(list(self.__window_shade_widgets.values())))