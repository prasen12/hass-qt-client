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

Created Date: Thursday, Mar 21st 2024, 5:54:58 pm

Author: Prasen Palvankar

----
Date Modified: Sun Jun 02 2024
Modified By: Prasen Palvankar
----
'''


import json
from PyQt5 import QtWebSockets, QtNetwork
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot

class HomeAssistantWSClient(QObject):
    __instance = None
    entity_state_changed = pyqtSignal(str, dict)
    areas_list_received = pyqtSignal(list)
    entities_list_received = pyqtSignal(list)
    entity_states_received = pyqtSignal(list)
    device_list_received = pyqtSignal(list)
    homeassistant_client_ready = pyqtSignal()
    homeassistant_connection_error = pyqtSignal(str)
    homeassistant_error_message = pyqtSignal(str)
    homeassistant_info_message = pyqtSignal(str)
    
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            super(QObject, cls.__instance).__init__()
        return cls.__instance
    
    # def __init__(self) -> None:
    #     super().__init__()
        # websocket.enableTrace(True)
       

    

            
    def __get_message_id(self):
        self.__messageId = self.__messageId + 1
        return self.__messageId
        
    def __handle_get_states_response(self, response:dict):
        print("---- got states ---")
        # print(json.dumps(response, indent=4))
        self.entity_states_received.emit(response['result'])


    def __handle_get_entities_response(self, response:dict):
        # cover_entities = []
        # light_entities = []
        # for e in filter(lambda x: (x['entity_id'].startswith('cover.') and x['attributes'].get('device_class') != 'garage'), response['result']):
        #     cover_entities.append(e)
        # self.cover_entities_received.emit(cover_entities)
        # for e in  filter(lambda x: (x['entity_id'].startswith('light.') and x['attributes'].get('device_class') != 'garage'), response['result']):
        #     light_entities.append(e)
        # self.light_entities_received.emit(light_entities)
        self.entities_list_received.emit(response['result'])
    
    def __handle_get_areas_response(self, response:dict):
        self.areas_list_received.emit(response['result'])
    
    def __handle_get_devices_response(self, response:dict):
        self.device_list_received.emit(response['result'])
        
    def __handle_subscribe_trigger_response(self, response:dict):
        print ('=== got subscribe trigger response === ')
        print (json.dumps(response, indent=4))
        if response['type'] == 'event':
            print ('===== got event ====')
            print (json.dumps(response, indent=4))
            trigger = response['event']['variables']['trigger']
            if trigger['platform'] == 'state':
                f = self.__stateChangeListeners[trigger['entity_id']]
                f(trigger['entity_id'], trigger['from_state']['state'], trigger['to_state']['state'])
                
    
    def __handle_state_changed_event(self, event:any):
        if event['type'] != 'event':
            return
        else:
            entity_id:str = event['event']['data']['entity_id']
            self.entity_state_changed.emit(entity_id, event['event']['data'])
            # if entity_id.startswith('cover.'):
            # self.cover_entity_state_changed.emit(entity_id, event['event']['data'])
     
    def __handle_service_response(self, data:any):
        print (data)
        
    def __handle_message(self, data:any ):
        # print(data)
        message = json.loads(data)
        if message['type'] == 'auth_required':
            self.__wsclient.sendTextMessage(json.dumps({"type": "auth", "access_token": self.__token}))
        elif message['type'] == 'auth_ok':
            self.__ready = True
            self.__send_message('subscribe_events', self.__handle_state_changed_event, {"event_type": "state_changed"})
            self.homeassistant_client_ready.emit()
        elif message['type'] == 'auth_invalid':
            print (f'Authorization invalid: {message["message"]}')
            self.homeassistant_error_message.emit(message['message'])
        elif message['type'] == 'result':
            if not message['success']:
                print (f'Received Error from Homeassistant: {message["error"]}')
                self.homeassistant_error_message.emit(message['message'])
            else:
                pr = self.__pendingRequests[message['id']]
                cb = pr.get('callback')
                if cb:
                    cb(message)
        elif message['type'] == 'event':
            pr = self.__pendingRequests[message['id']]
            pr['callback'](message)
   
    def __send_message(self, messageType: str, responseHandler, data:dict=None):
        print(f'send message {messageType} {data}')
        id = self.__get_message_id()
        mesg = {"id": id, "type": messageType}
        if (data):
            mesg.update(data)
        self.__wsclient.sendTextMessage(json.dumps(mesg))
        self.__pendingRequests[id] = {'type': messageType, 'callback': responseHandler}

    def get_states(self):
        self.__send_message('get_states', self.__handle_get_states_response)
    
    # def register_state_trigger_listener(self, entity_id: str, fromState:str, toState:str, listener):
    #     self.__stateChangeListeners[entity_id] = listener
    #     self.__send_message('subscribe_trigger', self.__handle_subscribe_trigger_response, {"trigger": {"platform": "state", "entity_id":  entity_id, "from": fromState, "to": toState}})
    
    def request_entities(self):
        # self.__send_message('get_states', self.__handle_get_entities_response)
        self.__send_message('config/entity_registry/list', self.__handle_get_entities_response)
    
    def request_areas(self):
        self.__send_message('config/area_registry/list', self.__handle_get_areas_response)
    
    def request_devices(self):
        self.__send_message('config/device_registry/list', self.__handle_get_devices_response)
        
    def set_cover_position(self, entity_id: str, position:int):
        serviceRequest = {
            "domain": "cover",
            "service": "set_cover_position",
            "service_data": {
                "position": position
            },
            "target": {
                "entity_id": entity_id
            }
        }
        self.__send_message('call_service', self.__handle_service_response, serviceRequest)
    
    def set_light_state(self, entity_id:str, state:str):
        serviceRequest = {
            "type": "call_service",
            "domain": "light",
            "service": "turn_on" if state == 'on' else "turn_off",
            "return_response": False,
            "service_data": {
                "entity_id": entity_id
            }
        }
        self.__send_message('call_service', self.__handle_service_response, serviceRequest)
        
    def connect(self, haUrl:str, token:str):
        self.__messageId = 0
        self.__wsclient = QtWebSockets.QWebSocket()
        self.__wsclient.error.connect(self.__handle_error)
        self.__wsclient.textMessageReceived.connect(self.__handle_message)
        self.__stateChangeListeners = dict()
        self.__pendingRequests = dict()
        self.__token = token
        self.__url = haUrl
        self.__wsclient.open(QUrl(haUrl))

        
    def __handle_error(self, data:QtNetwork.QAbstractSocket.SocketError):
        print (data)    
        self.homeassistant_connection_error.emit(self.__wsclient.errorString())


# app = QtWidgets.QApplication([])
# hawsclient = HomeAssistantWSClient('ws://homeassistant.local:8123/api/websocket', homeAssistantToken)


# haclient = HomeAssistantApiClient('http://homeassistant.local:8123')
# haclient.get_cover_entities('guestroom')