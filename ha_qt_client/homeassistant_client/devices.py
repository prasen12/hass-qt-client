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

Created Date: Friday, Apr 5th 2024, 5:42:00 pm

Author: Prasen Palvankar

----
Date Modified: Sun May 19 2024
Modified By: Prasen Palvankar
----
'''

from PyQt5.QtCore import QObject

from enum import Enum
from typing import Any, Optional, List
from PyQt5.QtCore import pyqtSignal,QObject
from ha_qt_client.homeassistant_client.websocket_client import HomeAssistantWSClient

class DisabledBy(Enum):
    CONFIG_ENTRY = "config_entry"


class EntryType(Enum):
    SERVICE = "service"




class Device:
    area_id: Optional[str]
    configuration_url: Optional[str]
    config_entries: List[str]
    connections: List[List[str]]
    disabled_by: Optional[DisabledBy]
    entry_type: Optional[EntryType]
    hw_version: Optional[str]
    id: str
    identifiers: List[List[str]]
    manufacturer: Optional[str]
    model: Optional[str]
    name_by_user: Optional[str]
    name: Optional[str]
    serial_number: Optional[str]
    sw_version: Optional[str]
    via_device_id: Optional[Any]

    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get('id')
        self.configuration_url = kwargs.get('configuration_url')
        self.config_entries = kwargs.get('config_entries')
        self.connections = kwargs.get('connections')
        self.disabled_by = kwargs.get('disabled_by')
        self.entry_type = kwargs.get('entry_type')
        self.hw_version = kwargs.get('hw_version')
        self.area_id = kwargs.get('area_id')
        self.identifiers = kwargs.get('identifiers')
        self.manufacturer = kwargs.get('manufacturer')
        self.model = kwargs.get('model')
        self.name_by_user = kwargs.get('name_by_user')
        self.name = kwargs.get('name')
        self.serial_number = kwargs.get('serial_number')
        self.sw_version = kwargs.get('sw_version')
        self.via_device_id = kwargs.get('via_device_id')

class DevicesManager(QObject):
    devices_updated = pyqtSignal()
    
    def __init__(self) -> None:
        super().__init__()
        hass_client = HomeAssistantWSClient.get_instance()
        self.__devices:dict[str,Device] = dict()
        hass_client.device_list_received.connect(self.__add_devices)
    
    def __add_devices(self, deviceList:list[dict]):
        for a  in deviceList:
            device = Device(**a)
            self.__devices[device.id] = device
        self.devices_updated.emit()
        
    def get_device(self, id:str):
        return self.__devices.get(id)
    
    def get_device_names(self) -> list[str]:
        return list(map(lambda x: x.name, self.__devices.values()))
