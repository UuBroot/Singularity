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
        self.guideLabelBox = QWidget()
        guideLabelBoxLayout = QHBoxLayout()
        guidelabel = QLabel("Drag and drop a file here")
        guidelabel.setAlignment(Qt.AlignCenter)  # Center the text
        guideLabelBoxLayout.addWidget(guidelabel)
        self.guideLabelBox.setLayout(guideLabelBoxLayout)

        self.layout.addWidget(self.guideLabelBox)
        
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
                            background-color: #5C5C5C;
                            border-radius:15px;
                            padding: 20px;

                           """)

    def dragEnterEvent(self, event):
        self.layout.setCurrentWidget(self.dragScreen)
        self.setStyleSheet("""
                            background-color: #292929;
                            border-radius:15px;
                            padding: 20px;
                            
                           """)
        
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.layout.setCurrentWidget(self.guidelabel)
        self.setStyleSheet("""
                            background-color: #5C5C5C;
                            border-radius:15px;
                            padding: 20px;
                            
                           """)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = self.getFilePath(urls[0])
                self.signal.emit(file_path)

    def getFilePath(self, url):
        return url.toLocalFile()
