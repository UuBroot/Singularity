from PySide6.QtCore import *

from global_vars import globals

import time

class WorkerThreadPercentageUpdaterThread(QThread):
    convertion_id: int
    percentageSignal = Signal(float)
    def __init__(self, convertion_id):
        super().__init__()
        self.convertion_id = convertion_id

    def run(self):
        while True:
            self.percentageSignal.emit(globals.get("percentageList").get(self.convertion_id))
            time.sleep(1)