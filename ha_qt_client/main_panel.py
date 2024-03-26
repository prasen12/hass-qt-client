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

Created Date: Tuesday, Mar 19th 2024, 10:05:54 pm

Author: Prasen Palvankar

----
Date Modified: Tue Mar 19 2024
Modified By: Prasen Palvankar
----
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from main_panel_frame import Ui_MainPanel

class MainPanel(QtWidgets.QFrame):
    
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_MainPanel()
        self.ui.setupUi(parent)

        
