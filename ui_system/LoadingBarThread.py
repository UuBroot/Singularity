from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class LoadingBarThread(QThread):
    update_value = pyqtSignal(int)

    def __init__(self):
         super().__init__()
         
    def run(self):
        while True:
            self.updateLoadingBar()
        
    def updateLoadingBar(self):
        try:
            self.update_value.emit(1)
        except Exception as e:
            print(e)
        self.sleep(1)
    