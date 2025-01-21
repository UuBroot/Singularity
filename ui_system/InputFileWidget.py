from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from global_vars import globals
from ui_system.Threads.WorkerThreadPercentageUpdaterThread import WorkerThreadPercentageUpdaterThread

class InputFileWidget(QWidget):
    fileSelected = Signal(str)
    convertion_id: int
    def __init__(self, convertion_id):
            super().__init__()
            self.initUI()
            self.convertion_id = convertion_id

            # percentage checker thread
            self.percentageCheckerThread = WorkerThreadPercentageUpdaterThread(self.convertion_id)
            self.percentageCheckerThread.percentageSignal.connect(self.setPercentage)
            self.percentageCheckerThread.start()

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

        #percentage
        self.percentage = QLabel()
        self.layout.addWidget(self.percentage)

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

    def setPercentage(self, percentage):
        if percentage == 0.0:
            self.percentage.setText("")
        else:
            self.percentage.setText(str(int(percentage))+"%")

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
        if globals.get("convertionInProgress"):
            print("cancel the operation first")
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error")
            msg_box.setText("You need to cancel all operation before deleting a file from the list")
            msg_box.exec_()
            return
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            try:
                self.deleteLater()
            except Exception as e:
                print(e)