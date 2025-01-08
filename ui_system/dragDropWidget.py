from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class DragDropWidget(QWidget):
    signal = Signal(str)
    file_path: str
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QStackedLayout()
        self.setLayout(self.layout)

        ##guide lable
        self.guidelabelBox = QWidget()
        self.guidelabelBoxLayout = QHBoxLayout()
        self.guidelabel = QLabel("Drag and drop a file here")
        self.guidelabel.setStyleSheet("""
                                 
                                 color: rgba(255, 255, 255, 0.7);
                                 
                                 """)
        self.guidelabel.setAlignment(Qt.AlignCenter)  # Center the text
        self.guidelabelBoxLayout.addWidget(self.guidelabel)
        self.guidelabelBox.setLayout(self.guidelabelBoxLayout)

        self.layout.addWidget(self.guidelabelBox)
        
        ##on drag screen
        self.dragScreen = QWidget()
        dragScreenLayout = QHBoxLayout()
        
        dragScreenLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        drag_icon = QLabel()
        drag_icon.setPixmap(QIcon.fromTheme("document-open").pixmap(64, 64))
        dragScreenLayout.addWidget(drag_icon)
        
        self.dragScreen.setLayout(dragScreenLayout)
        self.layout.addWidget(self.dragScreen)
        
        dragScreenLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.setAcceptDrops(True)
        self.setStyleSheet("""
                            background-color: rgba(92, 92, 92, 0.1);
                            border-radius:15px;
                            padding: 20px;

                           """)

    def dragEnterEvent(self, event):
        self.switchDragWidgetTo("dragScreen")
        
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.switchDragWidgetTo("guidelabelBox")

    def dropEvent(self, event):
        self.switchDragWidgetTo("guidelabelBox")
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = self.getFilePath(urls[0])
                self.signal.emit(file_path)

    def getFilePath(self, url):
        return url.toLocalFile()

    def switchDragWidgetTo(self, switchTo: str):
        match switchTo:
            case "guidelabelBox":
                self.layout.setCurrentWidget(self.guidelabelBox)
                self.setStyleSheet("""
                                    background-color: rgba(92, 92, 92, 0.1);
                                    border-radius:15px;
                                    padding: 20px;
                                    
                                """)
            case "dragScreen":
                self.layout.setCurrentWidget(self.dragScreen)
                self.setStyleSheet("""
                            background-color: rgba(41, 41, 41, 0.1);
                            border-radius:15px;
                            padding: 20px;
                            
                           """)
            case _:
                print("Invalid switchTo value")