from PySide6.QtCore import *

from global_vars import globals

class WorkerThreadFinishCheckerThread(QThread):
    finished = Signal()
    workerThreads = []
    def __init__(self, workerThreads):
         super().__init__()
         self.workerThreads = workerThreads
         
    def run(self):
        for thread in self.workerThreads:
                    thread.wait()
        globals.update(convertionInProgress=False)
        self.finished.emit()