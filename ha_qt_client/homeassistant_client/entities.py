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

Created Date: Sunday, Apr 7th 2024, 5:32:54 pm

Author: Prasen Palvankar

----
Date Modified: Mon May 20 2024
Modified By: Prasen Palvankar
----
'''


from typing import Type
from PyQt5.QtCore import QObject, pyqtSignal
from ha_qt_client.homeassistant_client.entity import Entity
from ha_qt_client.homeassistant_client.websocket_client import HomeAssistantWSClient
from ha_qt_client.homeassistant_client.entity import Entity
from PyQt5.QtCore import  pyqtSignal


class CoverEntity(Entity):
    open_position_updated = pyqtSignal(str, int)
    slider_position_changed = pyqtSignal(str, int)
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__open__position = None
    
    def set_state(self, state: any):
        super().set_state(state)
        curr_pos =  (self.state.get('attributes')).get('current_position')
        if curr_pos:
            self.__set_current_cover_position(curr_pos)
    
    @property
    def open_position(self):
        return self.__open__position
     
    def __set_current_cover_position(self, position: int):
        if position != self.__open__position:
            self.__open__position = position
            self.open_position_updated.emit(self.entity_id, position)
            
    def set_current_slider_position(self, position:int):
        if position != self.__open__position:
            self.__open__position = position
            self.homeassistant_client.set_cover_position(self.entity_id, position)


class LightEntity(Entity):
   def __init__(self, **kwargs) -> None:
       super().__init__(**kwargs)


class EntitiesManager(QObject):
    entities_updated = pyqtSignal()
    
    def __init__(self, entity_groups:list[str]) -> None:
        super().__init__()
        self.__entities:dict[str, Entity] = dict()
        self.__hass_client = HomeAssistantWSClient.get_instance()
        self.__hass_client.entities_list_received.connect(self.__add_entities)
        self.__hass_client.entity_state_changed.connect(self.__on_state_changed)
        self.__hass_client.entity_states_received.connect(self.__on_states_received)
        
        self.__entity_classes:dict[str, Type[Entity]] = {
            'cover': CoverEntity,
            'light': LightEntity
        }
        
    def __add_entities(self, data:list):
        for e in data:
            group:str = e['entity_id'].split('.')[0]
            entity_class = self.__entity_classes.get(group)
            if entity_class is not None:
                ec = entity_class(**e)                
                # new_entity = Entity(**e)   
                self.__entities[ec.entity_id] = ec         
        # Object for Entities we are interested are now created. Get the current states
        self.__hass_client.get_states()
        self.entities_updated.emit()

    def __on_states_received(self, states:list):
        # Create a filtered list of states for groups we support
        def groupFilterFunction(state:dict):
            group:str = state['entity_id'].split('.')[0]
            return group in self.__entity_classes.keys()
        
        filteredStates = filter(groupFilterFunction, states)
        for fs in filteredStates:
            entity = self.__entities.get(fs['entity_id'])
            if (entity):
                entity.set_state(fs)
            
    def __on_state_changed(self, entity_id:str, eventData:dict):
        e = self.get_entity(entity_id)
        if e is not None:
            e.set_state(eventData['new_state'])


    def get_entity(self, entity_id:str):
        return self.__entities.get(entity_id)

    def get_entities(self, group:str=None, area_id:str=None)->list[Entity]:
        if group is not None:
            if area_id is not None:
                return list(filter(lambda x: (x.entity_group == group and x.area_id == area_id) ,self.__entities.values()))
            else:
                return list(filter(lambda x: x.entity_group == group ,self.__entities.values()))
        else:
            return list(self.__entities.values())
    