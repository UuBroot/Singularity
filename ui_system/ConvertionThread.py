from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from system.main import convert

class ConvertionThread(QThread):
    filePathField: str
    pathOfExportField: str
    forceModule: str
    
    def __init__(self, filePathField, pathOfExportField, forceModule = None):
        super().__init__()
        self.filePathField = filePathField
        self.pathOfExportField = pathOfExportField
        self.forceModule = forceModule
    
    def run(self):
        convert(self.filePathField, self.pathOfExportField, self.forceModule)
        
    def stop(self):
        self.terminate()