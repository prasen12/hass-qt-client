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

Created Date: Friday, May 17th 2024, 4:24:49 pm

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''
from PyQt5.QtCore import QObject
from ha_qt_client.homeassistant_client.websocket_client import HomeAssistantWSClient

class Entity(QObject):
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.__area_id = kwargs['area_id']
        self.__device_id = kwargs['device_id']
        self.__entity_category = kwargs['entity_category']
        self.__entity_id = kwargs['entity_id']
        self.__name = kwargs.get('name')
        self.__original_name = kwargs.get('original_name')
        self.__platform = kwargs['platform']
        self.__state:dict = None
        self.__last_updated = None
        self.__last_changed = None
        self.__hass_client = HomeAssistantWSClient.get_instance()
    
    @property
    def homeassistant_client(self) -> HomeAssistantWSClient:
        return self.__hass_client
    
    @property
    def platform(self):
        return self.__platform
    
    @property
    def state(self):
        return self.__state
    
    @property
    def entity_id(self):
        return self.__entity_id
    
    @property 
    def entity_group(self):
        return self.__entity_id.split('.')[0] 
       
    @property
    def device_id(self):
        return self.__device_id

    @property
    def name(self):
        return self.__name if self.__name is not None else (self.__original_name if self.__original_name is not None else self.__entity_id)
    
    @property
    def last_changed(self):
        return self.__last_changed
    
    @property
    def last_updated(self):
        return self.__last_updated
    
    def set_state(self, state:dict):
        self.__state = state
    
    @property 
    def area_id(self):
        return self.__area_id

    @area_id.setter
    def area_id(self, id:str):
        self.__area_id = id