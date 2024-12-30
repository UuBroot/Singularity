import time
import sys
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from ui_system.dragDropWidget import DragDropWidget
from ui_system.ConvertionThread import ConvertionThread
from ui_system.LoadingBarThread import LoadingBarThread

from global_vars import globals
    
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
        path_of_file_select_button_icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)
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
        path_of_export_select_button_icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave)
        path_of_export_select_button.setIcon(path_of_export_select_button_icon)
        path_of_export_select_button.clicked.connect(self.select_export_path)
        pathOfExportLayout.addWidget(path_of_export_select_button)
        
        ##Conversion Buttons
        conversionButtonRow = QWidget()
        conversionButtonRowLayout = QHBoxLayout()
        conversionButtonRow.setLayout(conversionButtonRowLayout)

        #Cancel Convertion Button
        cancelConvertionButton = QPushButton()
        cancelConvertionButton.setText("Cancel")
        cancelConvertionButton.clicked.connect(self.cancelConvertion)
        conversionButtonRowLayout.addWidget(cancelConvertionButton)
        
        #ExportButton
        export_button = QPushButton()
        export_button_icon = QIcon.fromTheme(QIcon.ThemeIcon.GoNext)
        export_button.setIcon(export_button_icon)
        export_button.clicked.connect(self.export)
        conversionButtonRowLayout.addWidget(export_button)
        
        self.global_layout.addWidget(conversionButtonRow)
        
        ##AdvancedOptionsToggleBox
        advancedOptionsBox = QCheckBox()
        advancedOptionsBox.stateChanged.connect(self.toggle_advanced_options)
        self.global_layout.addWidget(advancedOptionsBox)
        
        #Advanced Options Box
        self.advancedOptionsContainer = QWidget()
        advancedOptionsContainerLayout = QHBoxLayout()
        self.advancedOptionsContainer.setVisible(False)
        self.advancedOptionsContainer.setLayout(advancedOptionsContainerLayout)
        self.advancedOptionsContainer.setMaximumHeight(40)
        self.global_layout.addWidget(self.advancedOptionsContainer)
        
        #Advanced module force selection
        self.forceModuleSelection = QComboBox()
        self.forceModuleSelection.addItem("none")
        self.forceModuleSelection.addItem("ffmpeg")
        self.forceModuleSelection.addItem("pillow")
        advancedOptionsContainerLayout.addWidget(self.forceModuleSelection)
        
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
        
        globals.update(finishedType=1)
        self.setFinishedMessage()
        
    def setFinishedMessage(self):
        if globals.get("finishedType") == 0:
            self.messageLabel.setText("Convertion finished")
        else:
            self.messageLabel.setText("Convertion canceled")
            
    def export(self):
        if self.pathOfExportField.text() != "" and self.filePathField.text() != "":
            if self.forceModuleSelection.currentText() == "None":
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
        globals.update(finishedType=0)
        
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
