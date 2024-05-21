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

Created Date: Saturday, Mar 30th 2024, 10:26:41 am

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''


from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from ha_qt_client.homeassistant_client.areas import AreasManager, Area
from ha_qt_client.homeassistant_client.devices import DevicesManager
from ha_qt_client.homeassistant_client.entities import EntitiesManager, CoverEntity
from ha_qt_client.widgets import covers_panel, controls_panel, rooms_panel
from ha_qt_client.homeassistant_client.websocket_client import HomeAssistantWSClient
from ha_qt_client.settings import settings

STATE_INITIALIZED = 'initialized'
STATE_COVERS_SELECTED = 'covers_selected'
STATE_SELECT_ENTITY_GROUP = 'select_entity_group'
STATE_SELECT_ROOMS = 'select_rooms'
STATE_ROOM_SELECTED = 'room_selected'


class HomeassistantQTClient(QtWidgets.QMainWindow):
    state_changed = pyqtSignal(str)
    
    def __init__(self) -> None:        
        super().__init__()            
        self.__setupMainWindow()
        
        self.__ha_ws_client = HomeAssistantWSClient.get_instance()
        self.__ha_ws_client.homeassistant_client_ready.connect(self.__handle_ha_client_ready)
        self.__ha_ws_client.homeassistant_connection_error.connect(self.__handle_ha_connection_error)
        self.__set_statusbar_text(f'Connecting to {settings.home_assistant_url}')
        self.__ha_ws_client.connect(settings.home_assistant_url, settings.home_assistant_token)
    
        self.__initial_load_status:dict[str,bool] = {
            "areas": False,
            "devices": False,
            "entities": False
        }
    
        self.__areas_manager = AreasManager()
        self.__areas_manager.areas_updated.connect(lambda : self.__set_initial_load_status('areas', True))
        self.__devices_manager = DevicesManager()
        self.__devices_manager.devices_updated.connect(lambda : self.__set_initial_load_status('devices', True))
        self.__entities_manager = EntitiesManager(['cover'])
        self.__entities_manager.entities_updated.connect(lambda : self.__set_initial_load_status('entities', True))
        self.__cover_panels:dict[str, covers_panel.CoversPanel] = dict()
        self.state_changed.connect(self.__change_state_to)

    def __setupMainWindow(self):
        self.resize(640, 480)
        self.__stacked_layout = QtWidgets.QStackedLayout()
        self.__main_widget = QtWidgets.QWidget(self)
        self.__main_widget.setLayout(self.__stacked_layout)
        self.setCentralWidget(self.__main_widget)
        self.__statusbar = QtWidgets.QStatusBar(self)
        self.__statusbar.setAutoFillBackground(False)
        self.__statusbar.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.__statusbar.setObjectName("__statusbar")
        self.__statusbar.resize
        self.setStatusBar(self.__statusbar)
    
    def __set_statusbar_text(self, txt:str):
        self.__statusbar.clearMessage()
        self.__statusbar.showMessage(txt)
        
    def __set_initial_load_status(self, name:str, status:bool):
        self.__initial_load_status[name] = status
        waiting_to_load = [*filter(lambda x: x == False, self.__initial_load_status.values())]
        if (len(waiting_to_load) == 0):
            self.__change_state_to(STATE_INITIALIZED)
           
            
        
    def __change_state_to(self, new_state:str):    
        if new_state == STATE_INITIALIZED:
            self.__set_statusbar_text('Connected.')
            self.__update_entities_room()
            self.__setup_areas_panel(self.__areas_manager.get_areas())
            self.__stacked_layout.addWidget(self.__rooms_panel)
            self.__stacked_layout.setCurrentWidget(self.__rooms_panel)
        elif new_state == STATE_ROOM_SELECTED:
            area_name = self.__areas_manager.get_area(self.__current_room_id).name
            self.__main_panel.setRoomName(area_name)
            self.__stacked_layout.setCurrentWidget(self.__main_panel)  
        elif new_state == STATE_COVERS_SELECTED:
            self.__stacked_layout.setCurrentWidget(self.__get_covers_panel())
        elif new_state == STATE_SELECT_ENTITY_GROUP:
            self.__stacked_layout.setCurrentWidget(self.__main_panel)
        elif new_state == STATE_SELECT_ROOMS:
            self.__stacked_layout.setCurrentWidget(self.__rooms_panel)
            
    
    def __setup_areas_panel(self, areas:list[Area]):
        self.__rooms_panel = rooms_panel.RoomsPanel(self)
        rooms = areas
        if len(settings.rooms_to_show) > 0 :
            rooms = list(filter(lambda x: x.name in settings.rooms_to_show, areas))
        self.__rooms_panel.add_rooms(rooms)
        self.__rooms_panel.room_selected.connect(self.__handle_room_selected)
       
    def __update_entities_room(self):
        cover_entities:list[CoverEntity] = self.__entities_manager.get_entities()
        for ce in cover_entities:
            device = self.__devices_manager.get_device(ce.device_id)
            if device is not None:
                ce.area_id = device.area_id
        
    @pyqtSlot()
    def __handle_ha_client_ready(self):
        self.__statusbar.clearMessage()
        self.__set_statusbar_text('Connected. Requesting configuration from Home Assitant...')
        self.__stacked_layout = QtWidgets.QStackedLayout()
        self.__main_panel = controls_panel.ControlsPanel(self)
        self.__main_panel.on_rooms_button_clicked(lambda x: self.__change_state_to(STATE_SELECT_ROOMS))
        self.__main_panel.on_shades_button_clicked(lambda x: self.__change_state_to(STATE_COVERS_SELECTED))
        self.__stacked_layout.addWidget(self.__main_panel)
        self.__ha_ws_client.request_areas()
        self.__ha_ws_client.request_devices()
        self.__ha_ws_client.request_entities()


    @pyqtSlot(str)
    def __handle_ha_connection_error(self, data:any):
        self.__set_statusbar_text(f'Connection to {settings.home_assistant_url} failed. Error: {data}')
    
    @pyqtSlot(str)
    def __handle_room_selected(self, room_id:str):
        self.__current_room_id = room_id
        self.__change_state_to(STATE_ROOM_SELECTED)
        
    @pyqtSlot(list)
    def __get_covers_panel(self): 
        
        cp = self.__cover_panels.get(self.__current_room_id)
        if not cp:
            cover_entities:list[CoverEntity] = self.__entities_manager.get_entities(group='cover', area_id=self.__current_room_id)
            cp = covers_panel.CoversPanel(self, room_name=(self.__areas_manager.get_area(self.__current_room_id)).name)
            self.__stacked_layout.addWidget(cp)
            cp.on_back_button_clicked(lambda x: self.__change_state_to(STATE_SELECT_ENTITY_GROUP))
            cp.add_cover_entities(cover_entities)
        return cp
