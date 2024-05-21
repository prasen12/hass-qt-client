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
Date Modified: Sun May 19 2024
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
        
        # self.setMinimumSize(QtCore.QSize(640, 480))
        # self.setMaximumSize(QtCore.QSize(640, 480))
        # layout_widget = QtWidgets.QWidget(self)
        # layout_widget.setGeometry(QtCore.QRect(0, 0, 641, 481))
        # layout_widget.setObjectName("layout_widget")
        
        # vertical_layout = QtWidgets.QVBoxLayout(layout_widget)
        # vertical_layout.setContentsMargins(0, 0, 0, 0)
        # vertical_layout.setSpacing(0)
        # vertical_layout.setObjectName("vertical_layout")
        
        # frame_header = QtWidgets.QFrame(layout_widget)
        # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        # size_policy.setHorizontalStretch(0)
        # size_policy.setVerticalStretch(0)
        # size_policy.setHeightForWidth(frame_header.sizePolicy().hasHeightForWidth())
        # frame_header.setSizePolicy(size_policy)
        # frame_header.setMaximumSize(QtCore.QSize(640, 20))
        # frame_header.setAutoFillBackground(False)
        # frame_header.setStyleSheet("background-color: rgb(255, 215, 50);")
        # frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        # frame_header.setObjectName("frame_header")
        # layout_widget1 = QtWidgets.QWidget(frame_header)
        # layout_widget1.setGeometry(QtCore.QRect(0, 0, 641, 29))
        # layout_widget1.setObjectName("layout_widget1")
        # header_horizontal_layout = QtWidgets.QHBoxLayout(layout_widget1)
        # header_horizontal_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        # header_horizontal_layout.setContentsMargins(0, 1, 5, 6)
        # header_horizontal_layout.setSpacing(2)
        # header_horizontal_layout.setObjectName("header_horizontal_layout")
        # self.__label_header = QtWidgets.QLabel(layout_widget1)
        # self.__label_header.setMaximumSize(QtCore.QSize(16777215, 22))
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(15)
        # font.setBold(True)
        # font.setItalic(False)
        # font.setKerning(False)
        # self.__label_header.setFont(font)
        # self.__label_header.setStyleSheet("")
        # self.__label_header.setAlignment(QtCore.Qt.AlignCenter)
        # self.__label_header.setObjectName("self.__label_header")
        # header_horizontal_layout.addWidget(self.__label_header)
        # vertical_layout.addWidget(frame_header)
        # frame_main_container = QtWidgets.QFrame(layout_widget)
        # frame_main_container.setStyleSheet("background-color: rgb(175, 172, 255);")
        # frame_main_container.setFrameShape(QtWidgets.QFrame.NoFrame)
        # frame_main_container.setFrameShadow(QtWidgets.QFrame.Raised)
        # frame_main_container.setObjectName("frame_main_container")
        # self.__grid_layout_widget = QtWidgets.QWidget(frame_main_container)
        # self.__grid_layout_widget.setGeometry(QtCore.QRect(0, 0, 641, 411))
        # self.__grid_layout_widget.setObjectName("gridLayoutWidget")
        # self.__grid_layout_main = QtWidgets.QGridLayout(self.__grid_layout_widget)
        # self.__grid_layout_main.setContentsMargins(0, 0, 0, 0)
        # self.__grid_layout_main.setSpacing(6)
        # self.__grid_layout_main.setObjectName("gridLayoutMain")
        # horizontal_layout_widget = QtWidgets.QWidget(frame_main_container)
        # horizontal_layout_widget.setGeometry(QtCore.QRect(0, 410, 641, 51))
        # horizontal_layout_widget.setObjectName("horizontal_layout_widget")
        
        # self.__hbox_layout_buttons = QtWidgets.QHBoxLayout(horizontal_layout_widget)
        # self.__hbox_layout_buttons.setContentsMargins(10, 0, 10, 0)
        # self.__hbox_layout_buttons.setSpacing(20)
        # self.__hbox_layout_buttons.setObjectName("__hbox_layout_buttons")
        
        # self.__button_back = QtWidgets.QPushButton(horizontal_layout_widget)
        # self.__button_back.setText('Back')
        # self.__button_back.setMinimumSize(QtCore.QSize(16777215, 30))
        # self.__button_back.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setPointSize(13)
        # font.setBold(True)
        # self.__button_back.setFont(font)
        # self.__button_back.setStyleSheet("background-color: rgb(16, 32, 255);color:rgb(255,255,255)")
        # self.__button_back.setObjectName("__button_back")
        # self.__hbox_layout_buttons.addWidget(self.__button_back)
        
        # self.__button_close_all = QtWidgets.QPushButton(horizontal_layout_widget)
        # self.__button_close_all.setMinimumSize(QtCore.QSize(16777215, 30))

        # self.__button_close_all.setText('Close All')
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setBold(True)
        # self.__button_close_all.setFont(font)
        # self.__button_close_all.setStyleSheet("background-color: rgb(255, 61, 125);color:rgb(255,255,255)")
        # self.__button_close_all.setObjectName("__button_close_all")
        # self.__hbox_layout_buttons.addWidget(self.__button_close_all)
        # self.__button_open_all = QtWidgets.QPushButton(horizontal_layout_widget)
        # font = QtGui.QFont()
        # font.setFamily("Arial")
        # font.setBold(True)
        
        # self.__button_open_all.setFont(font)
        # self.__button_open_all.setText('Open All')
        # self.__button_open_all.setMinimumSize(QtCore.QSize(16777215, 30))
        # self.__button_open_all.setStyleSheet("background-color: rgb(62, 132, 93);color:rgb(255,255,255)")
        # self.__button_open_all.setObjectName("__button_open_all")
        # self.__hbox_layout_buttons.addWidget(self.__button_open_all)
        # vertical_layout.addWidget(frame_main_container)

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