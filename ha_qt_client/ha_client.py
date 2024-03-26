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

Created Date: Thursday, Mar 21st 2024, 5:54:58 pm

Author: Prasen Palvankar

----
Date Modified: Sat Mar 23 2024
Modified By: Prasen Palvankar
----
'''


import json
from requests import get, post, Response
from PyQt5 import QtWebSockets, QtWidgets
from PyQt5.QtCore import QUrl

from entity import Entity


class HomeAssistantApiClient():
    
    def __init__(self, haUrl:str) -> None:
        self.__haUrl = haUrl.rstrip('/')
    
    def getCoverEntities(self, room:str) -> list:
        resp:Response = get(url=f'{self.__haUrl}/api/states',
                            headers={
                                "Authorization": f'Bearer '
                            })
        
        if resp.status_code != 200:
            raise Exception(f'Failed to get entities - {resp.text}')
        states = resp.json() 
        
        for e in filter(lambda s: s['entity_id'].startswith('cover.'), states):
            print (e)
        

class HomeAssistantWSClient():
    
    def __init__(self, haUrl:str, token:str) -> None:
        # websocket.enableTrace(True)
        self.__token = token
        self.__url = haUrl
        self.__messageId = 0
        self.__wsclient = QtWebSockets.QWebSocket()
        self.__wsclient.open(QUrl(haUrl))
        self.__wsclient.error.connect(self.__handleError)
        self.__wsclient.textMessageReceived.connect(self.__handleMessage)
        self.__stateChangeListeners = dict()
        self.__getEntitiesListeners = dict()
        self.__pendingRequests = dict()
        self.__responseHandlers = {
            'get_states':           self.__handleGetStatesResponse,
            'subscribe_trigger':    self.__handleSubscribeTriggerResponse
        }
        
    def connect(self):
        self.__wss.connect(self.__url)
        data = self.__wss.recv()
        message = json.loads(data)
        if message['type'] == 'auth_required':
            self.__wss.send(json.dumps({"type": "auth", "access_token": self.__token}))
            data = self.__wss.recv()
            if message['type'] == 'auth_ok':
                self.__ready = True
    
    def onReady(self, f):
        self.__onReadyCallback = f
            
    def __getMessageId(self):
        self.__messageId = self.__messageId + 1
        return self.__messageId
        
    def __handleGetStatesResponse(self, response:dict):
        print("---- got states ---")
        print(json.dumps(response, indent=4))

    def __handleGetCoverEntitiesResponse(self, response:dict):
        coverEntities:list[Entity] = []
        for e in filter(lambda x: (x['entity_id'].startswith('cover.') and x['attributes'].get('device_class') != 'garage'), response['result']):
            entity = Entity(entityId=e['entity_id'],
                            state=e.get('state'),
                            lastChanged=e.get('last_changed'),
                            lastUpdated=e.get('last_updated'),
                            currentPosition=e.get('attributes').get('current_position'),
                            friendlyName=e.get('attributes').get('friendly_name'))
            
            coverEntities.append(entity)
        f = self.__getEntitiesListeners.get('cover')
        if (f):
            f(coverEntities)
    
    def __handleSubscribeTriggerResponse(self, response:dict):
        print ('=== got subscribe trigger response === ')
        print (json.dumps(response, indent=4))
        if response['type'] == 'event':
            print ('===== got event ====')
            print (json.dumps(response, indent=4))
            trigger = response['event']['variables']['trigger']
            if trigger['platform'] == 'state':
                f = self.__stateChangeListeners[trigger['entity_id']]
                f(trigger['entity_id'], trigger['from_state']['state'], trigger['to_state']['state'])
                
    
    def __handleMessage(self, data:any ):
        # print(data)
        message = json.loads(data)
        if message['type'] == 'auth_required':
            self.__wsclient.sendTextMessage(json.dumps({"type": "auth", "access_token": self.__token}))
        elif message['type'] == 'auth_ok':
            self.__ready = True
            if (self.__onReadyCallback):
                self.__onReadyCallback()
                
        elif message['type'] == 'result':
            if not message['success']:
                print (f'Received Error from Homeassistant: {message["result"]}')
            else:
                pr = self.__pendingRequests[message['id']]
                pr['callback'](message)
        elif message['type'] == 'event':
            pr = self.__pendingRequests[message['id']]
            pr['callback'](message)
   
    def __sendMessage(self, messageType: str, responseHandler, data:dict=None):
        print(f'send message {messageType} {data}')
        id = self.__getMessageId()
        mesg = {"id": id, "type": messageType}
        if (data):
            mesg.update(data)
        self.__wsclient.sendTextMessage(json.dumps(mesg))
        self.__pendingRequests[id] = {'type': messageType, 'callback': responseHandler}
        
    def getStates(self):
        self.__sendMessage('get_states', self.__handleGetStatesResponse)
    
    def registerStateTriggerListener(self, entityId: str, fromState:str, toState:str, listener):
        self.__stateChangeListeners[entityId] = listener
        self.__sendMessage('subscribe_trigger', self.__handleSubscribeTriggerResponse, {"trigger": {"platform": "state", "entity_id":  entityId, "from": fromState, "to": toState}})
    
    def getCoverEntities(self, listener):
        self.__getEntitiesListeners['cover'] = listener
        self.__sendMessage('get_states', self.__handleGetCoverEntitiesResponse)

        
    def __handleError(self, data:any):
        print (data)    


# app = QtWidgets.QApplication([])
# hawsclient = HomeAssistantWSClient('ws://homeassistant.local:8123/api/websocket', homeAssistantToken)


# haclient = HomeAssistantApiClient('http://homeassistant.local:8123')
# haclient.getCoverEntities('guestroom')