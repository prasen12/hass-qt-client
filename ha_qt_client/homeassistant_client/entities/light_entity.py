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

Created Date: Sunday, Jun 2nd 2024, 5:22:52 pm

Author: Prasen Palvankar

----
Date Modified: Sun Jun 02 2024
Modified By: Prasen Palvankar
----
'''


from ha_qt_client.homeassistant_client.entity import Entity
from PyQt5.QtCore import  pyqtSignal


class LightEntity(Entity):
   light_entity_state_changed = pyqtSignal(str, str)

   def __init__(self, **kwargs) -> None:
       super().__init__(**kwargs)
       self.__switch_state = 'off'

   def set_state(self, state:str):
       super().set_state(state)
       self.__switch_state = self.state.get('state')
       self.light_entity_state_changed.emit(self.entity_id, self.__switch_state)

   @property
   def light_entity_state(self):
       return self.__switch_state
   
   @light_entity_state.setter
   def light_entity_state(self, state:str):
       self.__switch_state = state
       self.homeassistant_client.set_light_state(self.entity_id, state)