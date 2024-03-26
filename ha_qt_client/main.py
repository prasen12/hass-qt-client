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

Created Date: Tuesday, Mar 19th 2024, 7:03:10 pm

Author: Prasen Palvankar

----
Date Modified: Mon Mar 25 2024
Modified By: Prasen Palvankar
----
'''


import sys
from PyQt5 import QtCore, QtWidgets
from blinds_panel import BlindsPanel
from ha_client import HomeAssistantWSClient
from entity import Entity
from main_panel import MainPanel
from blinds_panel_frame import Ui_BlindsPanel
from main_panel_frame import Ui_MainPanel
homeAssistantToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyYzNmYmVjOThkNDA0N2I3YjcyZDUxM2ZiNjQ3Yzg5MSIsImlhdCI6MTcxMDczOTE2NSwiZXhwIjoyMDI2MDk5MTY1fQ.IiMgsY7vKUzLM_8kJVh8CS6c5npr8QMosOQqpgOHjHc'
currentRoom = 'family_room'
currentRoomName = 'Family Room'

class HomeassistantQTClient(QtWidgets.QMainWindow):
    
    def __init__(self) -> None:
        
        
        def haClientReadyListener():
            # self.__haWSclient.registerStateTriggerListener('light.office_desk_lamp_light_2', 'off', 'on', stateChangeListener)
            # self.__haWSclient.registerStateTriggerListener('light.office_desk_lamp_light_2', 'on', 'off', stateChangeListener)
            
            self.__haWSclient.getCoverEntities(self.__setupBlindsPanel)
            self.__stackedLayout = QtWidgets.QStackedLayout()
            qw = QtWidgets.QWidget()
            qw.setLayout(self.__stackedLayout)
            self.setCentralWidget(qw)
            
           
            mainPanel = Ui_MainPanel() 
            mainPanel.setupUi(self.__mainPanelFrame)
            mainPanel.blindsButton.clicked.connect(lambda x: self.__stackedLayout.setCurrentWidget(self.__blindsPanelFrame))
            
            self.__stackedLayout.addWidget(self.__mainPanelFrame)
            self.__stackedLayout.addWidget(self.__blindsPanelFrame)

            
    #     def stateChangeListener(entityId, fromState, toState):
    #             if fromState == 'off':
    #                 mainPanel.lightsButton.setStyleSheet("color: rgb(255, 255, 255);\n"
    # "color: rgb(15, 12, 90);\n"
    # "background-color: rgb(124, 255, 105);\n"
    # "font: 48pt \".AppleSystemUIFont\";")
    #             else:
    #                 mainPanel.lightsButton.setStyleSheet("color: rgb(255, 255, 255);\n"
    # "color: rgb(15, 12, 90);\n"
    # "background-color: rgb(124, 125, 105);\n"
    # "font: 48pt \".AppleSystemUIFont\";")
            
        super().__init__()
        self.resize(640, 480)
        self.__haWSclient = HomeAssistantWSClient('ws://homeassistant.local:8123/api/websocket', homeAssistantToken)
        self.__blindsPanelFrame = QtWidgets.QFrame()
        self.__mainPanelFrame = QtWidgets.QFrame()
        self.__haWSclient.onReady(haClientReadyListener)

    def __setupBlindsPanel(self, coverEntities:list[Entity]):
        row = 0
        col = 0
        blindsPanel = BlindsPanel(self.__blindsPanelFrame, roomName=currentRoomName)
        for e in filter(lambda x: (x.entityId.startswith(currentRoom)), coverEntities):
            blindsPanel.addBlind(e, row, col)
            col = col + 1
            if (col > 2):
                row = row + 1
                col = 0
    
        # blindsPanel.pushButton.clicked.connect(lambda x: self.__stackedLayout.setCurrentWidget(self.__mainPanelFrame))
        
    def run(self) -> int:
        # self.__mainPanel = MainPanel(self.__mainWindow)
        # self.__mainPanel.ui.blindsButton.clicked.connect(self.__showBlindsPanel)   
       
        return self.__qtApp.exec()


qtApp = QtWidgets.QApplication(sys.argv)
main =  HomeassistantQTClient()


main.show()

qtApp.exec()