import os
import sys
from PySide6.QtWidgets import *
from typing import List
from PySide6.QtGui import *
from PySide6.QtCore import *

from ui_system.dragDropWidget import DragDropWidget
from ui_system.Threads.ConvertionThread import ConvertionThread
from ui_system.Threads.WorkerThreadFinishCheckerThread import WorkerThreadFinishCheckerThread

from global_vars import globals, FinishedType

from ui_system.FfmpegNotInstalledPopup import FfmpegNotInstalledPopup
from ui_system.InputFileWidget import InputFileWidget

class MainWindow(QMainWindow):
    workerThreads: List[ConvertionThread] = []
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
        
        #PathOfFileLabel
        pathOfFileLabel = QLabel()
        pathOfFileLabel.setText("From:")
        pathOfFileRowLayout.addWidget(pathOfFileLabel)

        #PathOfFileColumn
        self.pathOfFileColumn = QWidget()
        self.pathOfFileColumnLayout = QVBoxLayout()
        self.pathOfFileColumn.setLayout(self.pathOfFileColumnLayout)
        pathOfFileRowLayout.addWidget(self.pathOfFileColumn)
        
        #Add a file button
        addInputButton = QPushButton()
        addInputButton.setText("Add File")
        addInputButton.clicked.connect(self.addNewFileInputUsingPicker)
        self.pathOfFileColumnLayout.addWidget(addInputButton)

        ##Arrow Down
        #ArrowDownRow
        arrow_down_row = QWidget()
        arrow_down_layout = QHBoxLayout()
        arrow_down_row.setLayout(arrow_down_layout)
        
        #Export Button
        arrow_down_label = QLabel()
        arrow_down_icon = QIcon.fromTheme("go-down")
        arrow_down_label.setPixmap(arrow_down_icon.pixmap(32, 32))
        arrow_down_label.setAlignment(Qt.AlignCenter)
        arrow_down_label.mousePressEvent = self.export
        arrow_down_label.setCursor(Qt.PointingHandCursor)
        arrow_down_layout.addWidget(arrow_down_label)
        
        self.global_layout.addWidget(arrow_down_row)
        
        ##PathOfExportRow
        pathOfExportRow = QWidget()
        pathOfExportLayout = QHBoxLayout()
        pathOfExportRow.setLayout(pathOfExportLayout)
        self.global_layout.addWidget(pathOfExportRow)
        pathOfExportRow.setMaximumHeight(50)

        #PathOfExportLabel
        pathOfExportLabel = QLabel()
        pathOfExportLabel.setText("To:")
        pathOfExportLayout.addWidget(pathOfExportLabel)
        
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
        self.advancedOptionsContainer.setMaximumHeight(70)
        self.global_layout.addWidget(self.advancedOptionsContainer)
        
        #Advanced module force selection
        forceModuleSelectionBox = QWidget()
        forceModuleSelectionBoxLayout = QHBoxLayout()
        forceModuleSelectionBox.setLayout(forceModuleSelectionBoxLayout)
        self.advancedOptionsContainerLayout.addWidget(forceModuleSelectionBox)
        
        forceModuleSelectionLabel = QLabel()
        forceModuleSelectionLabel.setText("Force Module")
        forceModuleSelectionBoxLayout.addWidget(forceModuleSelectionLabel)
        
        self.forceModuleSelection = QComboBox()
        self.forceModuleSelection.addItem("none")
        self.forceModuleSelection.addItem("ffmpeg")
        self.forceModuleSelection.addItem("pillow")
        self.forceModuleSelection.addItem("text")
        forceModuleSelectionBoxLayout.addWidget(self.forceModuleSelection)
        
        ##Loading Bar
        self.loadingBar = QProgressDialog()
        self.loadingBar.setAutoClose(False)
        self.loadingBar.setRange(0,0)
        self.loadingBar.setMaximumHeight(30)
        self.loadingBar.setCancelButton(None)
        self.global_layout.addWidget(self.loadingBar)
        
        #Cancel Convertion Button
        self.cancelConvertionButton = QPushButton()
        self.cancelConvertionButton.setText("Cancel")
        self.cancelConvertionButton.clicked.connect(self.cancelConvertion)
        self.cancelConvertionButton.hide()
        self.global_layout.addWidget(self.cancelConvertionButton)
        
        ##Message
        self.messageLabel = QLabel()
        self.messageLabel.setText("Press the arrow to convert")
        self.messageLabel.setMaximumHeight(20)
        self.global_layout.addWidget(self.messageLabel)
        
        ##Central Widget
        central_widget = QWidget()
        central_widget.setLayout(self.global_layout)
        self.setCentralWidget(central_widget)

        #DragNDrop Signal
        dropArea.signal.connect(self.addFileInputWidget)
    
    def addNewFileInputUsingPicker(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", "All Files (*)"
        )
        if path:
            self.addFileInputWidget(path)
    
    def addFileInputWidget(self, path = None):
        filePathFieldBox = InputFileWidget()
        filePathFieldBox.fileSelected.connect(self.updateExportPath)
        
        if type(path) == type(""):
            print(path)
            filePathFieldBox.setText(path)
            
        self.pathOfFileColumnLayout.addWidget(filePathFieldBox)
    
    def updateExportPath(self, path):
        path_parts = path.split("/")
        self.pathOfExportField.setText("/".join(path_parts[:-1])+"/")
        
    ###File Selection
    def select_export_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Select File", "", "All Files (*)"
        )
        if path:
            self.pathOfExportField.setText(path)
            
    def toggle_advanced_options(self):
        self.advancedOptionsContainer.setVisible(not self.advancedOptionsContainer.isVisible())
    
    def resetLoadingBar(self):
        self.loadingBar.setRange(0,0)
        self.loadingBar.hide()
        
    def hideLoadingBar(self):#needs to exist so that the bar gets hidden after first frame rendered
        self.loadingBar.hide()

    ###Convertion
    def convertationFinished(self):
        self.resetLoadingBar()
        self.setFinishedMessage()
        self.cancelConvertionButton.hide()
    
    def cancelConvertion(self):
        for worker_thread in self.workerThreads:
            worker_thread.terminate()
        self.resetLoadingBar()

        globals.update(finishedType=FinishedType.CANCELED)
        self.setFinishedMessage()
        self.cancelConvertionButton.hide()
        
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
            case FinishedType.FILENOTSUPPORTED:
                self.messageLabel.setText("One of the filetypes is not supported")
            case FinishedType.MODULENOTFOUNDERROR:
                try:
                    self.messageLabel.setText("Module not found:",str(globals.get("errorInModule")))
                except:
                    self.messageLabel.setText("Module not found")
                print(globals.get("errorInModule"))
                if globals.get("errorInModule") == "ffmpeg":
                    popup = FfmpegNotInstalledPopup()
                    popup.show()
            case FinishedType.NOPERMISSION:
                self.messageLabel.setText("No permission")
            case FinishedType.FILECORRUPT:
                self.messageLabel.setText("The file you are trying to read is corrupted")
            case _:
                self.messageLabel.setText("Unknown error")
            
    def export(self, event):
        if self.pathOfExportField.text() != "":#check if export field is empty
            if self.pathOfFileColumnLayout.count() <= 0:#check if files are used
                self.messageLabel.setText("Please add at least one file")
                return
        
            all_empty = False
            for i in range(self.pathOfFileColumnLayout.count()):
                widget: InputFileWidget = self.pathOfFileColumnLayout.itemAt(i).widget() 
                if isinstance(widget, InputFileWidget) and not os.path.exists(widget.getText()):#check if all files exists
                    all_empty = True
                    break

            if all_empty:
                self.messageLabel.setText("Please fill out all fields")
                return
        else:
            self.messageLabel.setText("Please fill out all fields")
            return

        #Addes the worker threads for every file
        for i in range(self.pathOfFileColumnLayout.count()):
            widget: InputFileWidget = self.pathOfFileColumnLayout.itemAt(i).widget()
            if isinstance(widget, InputFileWidget):
                exportPath: str = self.pathOfExportField.text()+"export"+str(i)+"."+widget.getFormat()
                if self.forceModuleSelection.currentText() == "none":#checks if a module is forced in advanced settings
                    self.workerThreads.append(ConvertionThread(widget.getText(), exportPath)) 
                else:
                    self.workerThreads.append(ConvertionThread(widget.getText(), exportPath, self.forceModuleSelection.currentText()))

        ##Threading
        self.cancelConvertionButton.show()
        
        for workerThread in self.workerThreads:
            workerThread.start()
        
        self.workerThreadChecker = WorkerThreadFinishCheckerThread(self.workerThreads)
        self.workerThreadChecker.finished.connect(self.convertationFinished)
        self.workerThreadChecker.start()
        
        self.messageLabel.setText("Converting...")
        globals.update(finishedType=FinishedType.FINISHED)
        
        self.loadingBar.show()
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Singularity")
    window.show()
    window.hideLoadingBar()
    sys.exit(app.exec())
