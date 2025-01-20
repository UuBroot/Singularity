from PySide6.QtCore import *

class WorkerThreadFinishCheckerThread(QThread):
    finished = Signal()
    workerThreads = []
    def __init__(self, workerThreads):
         super().__init__()
         self.workerThreads = workerThreads
         
    def run(self):
        for thread in self.workerThreads:
                    thread.wait()
        self.finished.emit()