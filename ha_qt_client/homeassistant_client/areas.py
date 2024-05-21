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

Created Date: Friday, Apr 5th 2024, 6:12:09 pm

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''

from typing import List, Any, Optional
from PyQt5.QtCore import pyqtSignal,QObject
from ha_qt_client.homeassistant_client.websocket_client import HomeAssistantWSClient

class Area:
    aliases: List[Any]
    area_id: str
    icon: str
    name: str
    picture: str

    def __init__(self, **kwargs):
        self.aliases = kwargs.get('aliases')
        self.area_id = kwargs.get('area_id')
        self.icon = kwargs.get('icon')
        self.name = kwargs.get('name')
        self.picture = kwargs.get('picture')


class AreasManager(QObject):
    areas_updated = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        self.__areas:dict[str,Area] = dict()
        hass_client = HomeAssistantWSClient.get_instance()
        hass_client.areas_list_received.connect(self.__add_areas)
    
    def __add_areas(self, areaList:list[dict]):
        for a  in areaList:
            area = Area(**a)
            self.__areas[area.area_id] = area
        self.areas_updated.emit()
    
    def get_area(self, area_id):
        return self.__areas.get(area_id)
    
    def get_areas(self) -> list[Area]:
        return list(self.__areas.values())
    
    def get_area_names(self) -> list[str]:
        return list(map(lambda x: x.name, self.__areas.values()))
    
        