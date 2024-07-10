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

Created Date: Saturday, May 25th 2024, 10:46:07 am

Author: Prasen Palvankar

----
Date Modified: Sun Jun 02 2024
Modified By: Prasen Palvankar
----
'''


from collections.abc import Callable
from typing_extensions import Self
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import resources.lights_rc

class LightSwitchWidget(QtWidgets.QFrame):
    light_switch_state_changed = pyqtSignal(str, str)
    
   
    switch_button_style = 'background-color: rgb(65, 113, 255)'
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('qtdesigns/light_switch_widget.ui', self)
        self.__button_light_switch = self.findChild(QtWidgets.QPushButton, 'pushButton_lightSwitch')
        self.__label_name = self.findChild(QtWidgets.QLabel, 'label_name')
        self.__label_light_state = self.findChild(QtWidgets.QLabel, 'label_lightState')
        self.__light_switch_state = 'off'
      
        self.__button_light_switch.clicked.connect(self.__toggle_state)
        self.__light_state_icons = {
            "off": {"icon": QtGui.QIcon(":images/light-bulb-off.png"), "label": "Off"},
            "unavailable": {"icon": QtGui.QIcon(":images/light-bulb-off.png"), "label": "Unavailable"},
            "on":  {"icon": QtGui.QIcon(":images/light-bulb-on.png"), "label": "On"}
        }
        
        self.__set_visual_state()

    def __set_visual_state(self):
        self.__label_light_state.setText(self.__light_state_icons[self.light_switch_state]['label'])
        self.__button_light_switch.setIcon(self.__light_state_icons[self.light_switch_state]['icon'])
        self.__button_light_switch.setEnabled(self.__light_switch_state != 'unavailable')
    
    def on_light_switch_clicked(self, fn:Callable[[int, Self]]):
        self.__button_light_switch.clicked.connect(lambda x:fn(self))
    
    @property
    def light_switch_state(self):
        return self.__light_switch_state

    @light_switch_state.setter
    def light_switch_state(self, state:str):
        self.__light_switch_state = state
        self.__set_visual_state()
      
    
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
        
    @pyqtSlot()
    def __toggle_state(self):
        if self.__light_switch_state != 'unavailable':
            self.__light_switch_state = 'off' if self.__light_switch_state == 'on' else 'on'
            self.light_switch_state_changed.emit(self.__entity_id, self.__light_switch_state)
            self.__set_visual_state()
            
            
        


