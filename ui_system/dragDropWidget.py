from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

class DragDropWidget(QWidget):
    signal = pyqtSignal(str)

    file_path: str
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop a file here")
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: gray;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ingore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = self.getFilePath(urls[0])
                self.signal.emit(file_path)

    def getFilePath(self, url):
        return url.toLocalFile()
