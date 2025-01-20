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
    convertion_id: int
    def __init__(self, filePathField, pathOfExportField, forceModule = None, convertion_id = 0):
        super().__init__()
        self.main = Main(convertion_id)
        self.filePathField = filePathField
        self.pathOfExportField = pathOfExportField
        self.forceModule = forceModule
        self.convertion_id = convertion_id
    
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

    def getId(self):
        return self.convertion_id