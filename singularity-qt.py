import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from uielements.dragDropWidget import DragDropWidget
from system.main import convert

class ConvertionThread(QThread):
    filePathField:str
    pathOfExportField:str
    forceModule:str
    
    def __init__(self, filePathField, pathOfExportField, forceModule):
        super().__init__()
        self.filePathField = filePathField
        self.pathOfExportField = pathOfExportField
        self.forceModule = forceModule
    
    def run(self):
        convert(self.filePathField, self.pathOfExportField, self.forceModule)

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

        #ExportButton
        export_button = QPushButton()
        export_button_icon = QIcon.fromTheme(QIcon.ThemeIcon.GoNext)
        export_button.setIcon(export_button_icon)
        export_button.clicked.connect(self.export)
        pathOfExportLayout.addWidget(export_button)
        
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
        ##Central Widget
        central_widget = QWidget()
        central_widget.setLayout(self.global_layout)
        self.setCentralWidget(central_widget)

        #DragNDrop Signal
        dropArea.signal.connect(self.updateFilePathField)
        
    def hideLoadingBar(self):#needs to exist so that the bar gets hiden after first frame rendered
        self.loadingBar.hide()
    
    def updateFilePathField(self, message):
        self.filePathField.setText(message)

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
        
    def export(self):
        if self.pathOfExportField.text() != "" and self.filePathField.text() != "":
            if self.forceModuleSelection.currentText() == "None":
                convert(self.filePathField.text(), self.pathOfExportField.text())
        convert(self.filePathField.text(), self.pathOfExportField.text(), self.forceModuleSelection.currentText())
        
        ##Threading
        self.worker_thread = ConvertionThread(self.filePathField.text(), self.pathOfExportField.text(), self.forceModuleSelection.currentText())
        self.worker_thread.finished.connect(self.convertationFinished)
        self.worker_thread.start()
        
        self.loadingBar.show()
        
    def convertationFinished(self):
        self.loadingBar.hide()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Singularity")
    window.show()
    window.hideLoadingBar()
    sys.exit(app.exec())