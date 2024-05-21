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

Created Date: Tuesday, Mar 19th 2024, 10:11:02 pm

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''
from collections.abc import Callable
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from ha_qt_client.temp.blinds_panel_frame import Ui_BlindsPanel
from ha_qt_client.temp.cover_entity import CoverEntity
from ha_qt_client.widgets.window_shade_widget import WindowShadeWidget
from ha_qt_client.widgets.window_shades_panel import WindowShadesPanel

class CoversPanel(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget, room_name:str) -> None:
        super().__init__(parent)
        self.resize(640, 480)
        self.__cover_entities:dict[str, CoverEntity] = dict()
        self.__setup_ui(room_name)

    def __setup_ui(self, room_name):
        self.__shades_panel = WindowShadesPanel(self)
        self.__shades_panel.header_text = room_name
        self.__shades_panel.on_close_all_clicked(self.__handle_close_all)
        self.__shades_panel.on_open_all_clicked(self.__handle_open_all)
    
    def set_current_position(self, cover_entities:list[CoverEntity]):
        for cover_entity in cover_entities:
            windowShadeWidget:WindowShadeWidget = self.__cover_entities(cover_entity.entity_id)
            windowShadeWidget.slider_position = cover_entity.open_position
    
    def on_back_button_clicked(self, fn:Callable):
        self.__shades_panel.on_back_clicked(fn)
        
    def __handle_close_all(self, wswList:list[WindowShadeWidget]):
        for wsw in wswList:
            wsw.slider_position = 0
    
    def __handle_open_all(self, wswList:list[WindowShadeWidget]):
        for wsw in wswList:
            wsw.slider_position = 100
    
    def __handle_slider_position_changed(self, position:int, wsw:WindowShadeWidget):
        print(wsw.entity_id, position)
        ce = self.__cover_entities.get(wsw.entity_id)
        if (ce):
            ce.set_current_slider_position(position)

    @pyqtSlot(str, int)
    def __handle_cover_entity_position_changed(self, entity_id:str, position:int):
        wsw = self.__shades_panel.get_window_shade_widget(entity_id)
        if wsw and wsw.slider_position != position:
            wsw.slider_position = position
            
    def __handle_close_clicked(self, wsw:WindowShadeWidget):
        ce = self.__cover_entities.get(wsw.entity_id)
        if (ce):
            ce.set_current_slider_position(0)
    
    def __handle_open_clicked(self, wsw:WindowShadeWidget):
        ce = self.__cover_entities.get(wsw.entity_id)
        if (ce):
            ce.set_current_slider_position(100)
            
    def __add_blind(self, cover_entity: CoverEntity, row: int, col: int):
        wsw = WindowShadeWidget()
        wsw.name = cover_entity.name
        wsw.entity_id = cover_entity.entity_id
        cover_entity.open_position_updated.connect(self.__handle_cover_entity_position_changed)
        wsw.slider_position = cover_entity.open_position
        wsw.on_slider_position_changed(self.__handle_slider_position_changed)
        wsw.on_close_clicked(self.__handle_close_clicked)
        wsw.on_open_clicked(self.__handle_open_clicked)
        self.__cover_entities[cover_entity.entity_id] = cover_entity
        self.__shades_panel.add_window_shade_widget(wsw, row, col)
        
    def add_cover_entities(self, cover_entities:list[CoverEntity]):
        row = col = 0
        for e in cover_entities:
            self.__add_blind(e, row, col)
            col = col + 1
            if (col > 2):
                row = row + 1
                col = 0
        



