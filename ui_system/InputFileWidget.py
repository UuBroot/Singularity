from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from global_vars import globals

class InputFileWidget(QWidget):
    fileSelected = Signal(str)
    def __init__(self):
            super().__init__()
            self.initUI()
    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
        self.filePathField = QLineEdit()
        self.filePathField.setPlaceholderText("Path to file")
        self.layout.addWidget(self.filePathField)
        
        #openFileButton
        openFileButton = QPushButton()
        openFileButton_icon = QIcon.fromTheme("document-open")
        openFileButton.setIcon(openFileButton_icon)
        openFileButton.clicked.connect(self.select_input_path)
        self.layout.addWidget(openFileButton)
        
        #Seperator
        seperator = QLabel()
        seperator.setMaximumWidth(40)
        self.layout.addWidget(seperator)
        
        #Format Field
        self.exportFormat = QLineEdit()
        self.exportFormat.setPlaceholderText("Export Format")
        self.exportFormat.setMaximumWidth(120)
        self.layout.addWidget(self.exportFormat)
        
        #delete widget button
        filePathField = QPushButton()
        filePathField.setIcon(QIcon.fromTheme("window-close"))
        filePathField.setFixedSize(QSize(32, 32))
        filePathField.setStyleSheet("background: transparent; border: none;")
        filePathField.clicked.connect(self.delete_self)
        self.layout.addWidget(filePathField)
    
    def setText(self, text):
        self.filePathField.setText(text)
        self.fileSelected.emit(text)#sets the export path

    def getText(self) -> str:
        return self.filePathField.text()
    
    def getFormat(self) -> str:
        return self.exportFormat.text()
    
    def select_input_path(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)"
        )
        if path:
            self.setText(path)
            
    def delete_self(self):
        print(globals.get("finishedType"))
        if globals.get("convertionInProgress"):
            print("cancel the operation first")
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("Please cancel the conversion before deleting a file from the list of files to convert")
            msg_box.exec_()
            return
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)