from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from system.main import Main

from global_vars import globals

class ConvertionThread(QThread):
    main: Main
    filePathField: str
    pathOfExportField: str
    forceModule: str
    id: int
    def __init__(self, filePathField, pathOfExportField, forceModule = None, id = 0):
        super().__init__()
        self.main = Main(id)
        self.filePathField = filePathField
        self.pathOfExportField = pathOfExportField
        self.forceModule = forceModule
        self.id = id
    
    def run(self):
        globals.update(convertionInProgress=True)
        try:
            self.main.convert(self.filePathField, self.pathOfExportField, self.forceModule)
            globals.update(convertionInProgress=False)
        except Exception as e:
            print(e)
        
    def stop(self):
        globals.update(convertionInProgress=False)
        self.main.terminate()#terminate other processes
        self.terminate()#terminaes the thread itself