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

Created Date: Saturday, May 25th 2024, 10:36:47 am

Author: Prasen Palvankar

----
Date Modified: Sun Jun 02 2024
Modified By: Prasen Palvankar
----
'''


from PyQt5 import QtWidgets, uic

from ha_qt_client.homeassistant_client.entities.light_entity import LightEntity
from ha_qt_client.widgets import light_switch_widget
from collections.abc import Callable

class LightsPanel(QtWidgets.QFrame):
    
    def __init__(self, parent: QtWidgets.QWidget, room_name:str) -> None:
        super().__init__(parent)
        
        self.__light_switch_widgets:dict[str, light_switch_widget.LightSwitchWidget] = dict()
        self.__light_switch_entities:dict[str, LightEntity] = dict()
        self.resize(640, 480)
        uic.loadUi('qtdesigns/lights_panel.ui', self)
        
        self.__label_header = self.findChild(QtWidgets.QLabel, 'label_headerText')
        self.__grid_layout_main = self.findChild(QtWidgets.QGridLayout, 'gridLayout_lightsWidget')
        self.__button_back = self.findChild(QtWidgets.QPushButton, 'pushButton_back')
        self.__button_turn_off_all = self.findChild(QtWidgets.QPushButton, 'pushButton_turnOffAll')
        self.__button_turn_on_all = self.findChild(QtWidgets.QPushButton, 'pushButton_turnOnAll')
        self.__label_header.setText(room_name)
        self.__button_turn_off_all.clicked.connect(lambda x: self.__set_state_for_all('off'))
        self.__button_turn_on_all.clicked.connect(lambda x: self.__set_state_for_all('on'))
        
    @property
    def header_text(self):
        return self.__label_header.text()
    
    @header_text.setter
    def header_text(self, s:str):
        self.__label_header.setText(s)
        
    def get_light_switch_widget(self, entity_id:str):
        return self.__light_switch_widgets.get(entity_id)

    def on_back_button_clicked(self, fn:Callable):
        self.__button_back.clicked.connect(fn)
        
    def __set_state_for_all(self, state:str):
       for ls in list(self.__light_switch_widgets.values()):
           le = self.__light_switch_entities.get(ls.entity_id)
           if le:
               le.light_entity_state = state
        #    ls.light_switch_state = state
    
    def __handle_light_state_change(self, entity_id:str, state:str):
        le = self.__light_switch_entities.get(entity_id)
        if le:
            le.light_entity_state = state
        
    def __handle_light_entity_state_change(self, entity_id:str, state:str):
        lsw = self.__light_switch_widgets.get(entity_id)
        if lsw:
            lsw.light_switch_state = state
            
    def __add_light_switch_widget(self, light_entity:LightEntity, row:int, col:int):
        lsw = light_switch_widget.LightSwitchWidget()       
        lsw.name = light_entity.name
        lsw.entity_id = light_entity.entity_id
        light_entity.light_entity_state_changed.connect(self.__handle_light_entity_state_change)
        lsw.light_switch_state_changed.connect(self.__handle_light_state_change)
        self.__grid_layout_main.addWidget(lsw, row, col, 1, 1)
        self.__light_switch_widgets[lsw.entity_id] = lsw
        self.__light_switch_entities[light_entity.entity_id] = light_entity
        
    def add_light_entities(self, light_entities:list[LightEntity]):
        row = col = 0
        for l in light_entities:
            self.__add_light_switch_widget(l, row, col)
            col = col + 1
            if col > 3:
                row = row + 1
                col = 0