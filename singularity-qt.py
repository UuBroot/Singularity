import time
import sys
import threading
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from ui_system.dragDropWidget import DragDropWidget
from ui_system.ConvertionThread import ConvertionThread
from ui_system.LoadingBarThread import LoadingBarThread

from global_vars import globals, FinishedType
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
                
        self.resize(800, 600)
        self.global_layout = QVBoxLayout()

        #DragNDrop Area
        dropArea = DragDropWidget()
        self.global_layout.addWidget(dropArea)

        ##PathOfFileRow
        pathOfFileRow = QWidget()
        pathOfFileRowLayout = QHBoxLayout()
        pathOfFileRow.setLayout(pathOfFileRowLayout)
        self.global_layout.addWidget(pathOfFileRow)
        pathOfFileRow.setMaximumHeight(50)

        #PathOfFileToConvertField
        self.filePathField = QLineEdit()
        self.filePathField.setPlaceholderText("Path to file")
        pathOfFileRowLayout.addWidget(self.filePathField)

        #PathOfFileButton
        path_of_file_select_button = QPushButton()
        path_of_file_select_button_icon = QIcon.fromTheme("document-open")
        path_of_file_select_button.setIcon(path_of_file_select_button_icon)
        path_of_file_select_button.clicked.connect(self.select_input_path)
        pathOfFileRowLayout.addWidget(path_of_file_select_button)

        ##PathOfExportRow
        pathOfExportRow = QWidget()
        pathOfExportLayout = QHBoxLayout()
        pathOfExportRow.setLayout(pathOfExportLayout)
        self.global_layout.addWidget(pathOfExportRow)
        pathOfExportRow.setMaximumHeight(50)

        #PathOfExportField
        self.pathOfExportField = QLineEdit()
        self.pathOfExportField.setPlaceholderText("Path to export")
        pathOfExportLayout.addWidget(self.pathOfExportField)

        #PathOfFileButton
        path_of_export_select_button = QPushButton()
        path_of_export_select_button_icon = QIcon.fromTheme("document-save")
        path_of_export_select_button.setIcon(path_of_export_select_button_icon)
        path_of_export_select_button.clicked.connect(self.select_export_path)
        pathOfExportLayout.addWidget(path_of_export_select_button)
        
        ##Conversion Buttons
        conversionButtonRow = QWidget()
        conversionButtonRowLayout = QHBoxLayout()
        conversionButtonRow.setLayout(conversionButtonRowLayout)
        conversionButtonRow.setMaximumHeight(50)

        #Cancel Convertion Button
        cancelConvertionButton = QPushButton()
        cancelConvertionButton.setText("Cancel")
        cancelConvertionButton.clicked.connect(self.cancelConvertion)
        conversionButtonRowLayout.addWidget(cancelConvertionButton)
        
        #ExportButton
        export_button = QPushButton()
        export_button_icon = QIcon.fromTheme("go-next")
        export_button.setIcon(export_button_icon)
        export_button.clicked.connect(self.export)
        conversionButtonRowLayout.addWidget(export_button)
        
        self.global_layout.addWidget(conversionButtonRow)
        
        ##AdvancedOptionsToggleBox
        advancedOptionsRow = QWidget()
        advancedOptionsRowLayout = QHBoxLayout()
        advancedOptionsRow.setLayout(advancedOptionsRowLayout)
        advancedOptionsRow.setMaximumHeight(50)
        self.global_layout.addWidget(advancedOptionsRow)
        
        advancedOptionsBox = QCheckBox()
        advancedOptionsBox.setMaximumWidth(20)
        advancedOptionsBox.stateChanged.connect(self.toggle_advanced_options)
        advancedOptionsRowLayout.addWidget(advancedOptionsBox)
        
        advancedOptionsLabl = QLabel()
        advancedOptionsLabl.setText("Advanced Options")
        advancedOptionsRowLayout.addWidget(advancedOptionsLabl)
        
        #Advanced Options Box
        self.advancedOptionsContainer = QWidget()
        self.advancedOptionsContainerLayout = QHBoxLayout()
        self.advancedOptionsContainer.setVisible(False)
        self.advancedOptionsContainer.setLayout(self.advancedOptionsContainerLayout)
        self.advancedOptionsContainer.setMaximumHeight(50)
        self.global_layout.addWidget(self.advancedOptionsContainer)
        
        #Advanced module force selection
        self.forceModuleSelection = QComboBox()
        self.forceModuleSelection.setMaximumHeight(30)
        self.forceModuleSelection.addItem("none")
        self.forceModuleSelection.addItem("ffmpeg")
        self.forceModuleSelection.addItem("pillow")
        self.advancedOptionsContainerLayout.addWidget(self.forceModuleSelection)
        
        ##Loading Bar
        self.loadingBar = QProgressDialog()
        self.loadingBar.setAutoClose(False)
        self.loadingBar.setRange(0,0)
        self.loadingBar.setMaximumHeight(30)
        self.loadingBar.setCancelButton(None)
        self.global_layout.addWidget(self.loadingBar)
        
        ##Message
        self.messageLabel = QLabel()
        self.messageLabel.setMaximumHeight(20)
        self.global_layout.addWidget(self.messageLabel)
        
        ##Central Widget
        central_widget = QWidget()
        central_widget.setLayout(self.global_layout)
        self.setCentralWidget(central_widget)

        #DragNDrop Signal
        dropArea.signal.connect(self.updateFilePathField)
    
    def updateFilePathField(self, message):
        self.filePathField.setText(message)
        message_parts = message.split("/") # Split the path into an array and remove the last element
        self.pathOfExportField.setText("/".join(message_parts[:-1])+"/")
        
    ###File Selection
    def select_input_path(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)"
        )
        if path:
            self.updateFilePathField(path)

    def select_export_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Select File", "", "All Files (*)"
        )
        if path:
            self.pathOfExportField.setText(path)
            
    def toggle_advanced_options(self):
        self.advancedOptionsContainer.setVisible(not self.advancedOptionsContainer.isVisible())
        
    ###Loading Bar
    def updateLoadingBar(self):
        print("updating loading bar",globals.get("current_percentage"))
        if globals.get("current_percentage") != 0.0:
            self.loadingBar.setRange(0,100)
            self.loadingBar.setValue(int(globals.get("current_percentage")))
    
    def resetLoadingBar(self):
        self.loadingBar.setRange(0,0)
        self.loadingBar.hide()
        globals.update(current_percentage=0.0)
        
    def hideLoadingBar(self):#needs to exist so that the bar gets hiden after first frame rendered
        self.loadingBar.hide()

    ###Convertion
    def convertationFinished(self):
        self.updateLoadingBarThread.terminate()
        self.resetLoadingBar()
        
        self.setFinishedMessage()
    
    def cancelConvertion(self):
        self.worker_thread.terminate()
        self.updateLoadingBarThread.terminate()
        self.resetLoadingBar()
        
        globals.update(finishedType=FinishedType.CANCELED)
        self.setFinishedMessage()
        
    def setFinishedMessage(self):
        match globals.get("finishedType"):
            case FinishedType.FINISHED:
                self.messageLabel.setText("Convertion finished")
            case FinishedType.CANCELED:
                self.messageLabel.setText("Convertion canceled")
            case FinishedType.NOTAVALIDFILE:
                self.messageLabel.setText("Not a valid file")
            case FinishedType.WRONGCOMBINATION:
                self.messageLabel.setText("Wrong combination of file used and format to convert to")
            case _:
                self.messageLabel.setText("Unknown error")
            
    def export(self):
        if self.pathOfExportField.text() != "" and self.filePathField.text() != "":
            print(self.forceModuleSelection.currentText())
            if self.forceModuleSelection.currentText() == "none":
                self.worker_thread = ConvertionThread(self.filePathField.text(), self.pathOfExportField.text())
            else:
                self.worker_thread = ConvertionThread(self.filePathField.text(), self.pathOfExportField.text(), self.forceModuleSelection.currentText())
        else:
            self.messageLabel.setText("Please fill all fields")
            return
        ##Threading
        self.worker_thread.finished.connect(self.convertationFinished)
        
        self.worker_thread.start()
        
        self.messageLabel.setText("Converting...")
        globals.update(finishedType=FinishedType.FINISHED)
        
        self.loadingBar.show()
        
        self.updateLoadingBarThread = LoadingBarThread()
        self.updateLoadingBarThread.update_value.connect(self.updateLoadingBar)
        self.updateLoadingBarThread.start()
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Singularity")
    window.show()
    window.hideLoadingBar()
    sys.exit(app.exec())
