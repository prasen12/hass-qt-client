'''
MIT License

Copyright (c) 2024 Oracle

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

Created Date: Friday, Mar 22nd 2024, 11:15:10 pm

Author: Prasen Palvankar

----
Date Modified: Sat Mar 23 2024
Modified By: Prasen Palvankar
----
'''


class Entity():
    
    def __init__(self, entityId:str, state:str=None, currentPosition:int=0, lastChanged:str=None, lastUpdated:str=None, friendlyName:str=None) -> None:
        self.__entityId = entityId
        self.__state = state
        self.__lastUpdated = lastUpdated
        self.__lastChanged = lastChanged
        self.__friendlyName = friendlyName
        self.__position = currentPosition
    
    @property
    def entityId(self):
        return self.__entityId.split('.')[1]
    
    @property
    def state(self):
        return self.__state
    
    @property
    def lastChanged(self):
        return self.__lastChanged
    
    @property
    def group(self):
        return self.__entityId.split('.')[0]
    
    @property
    def name(self):
        return self.__friendlyName
    @property
    def lastUpdated(self):
        return self.__lastUpdated
    
    @property
    def currentPosition(self):
        return self.__position
    
    