from PySide6.QtWidgets import  QMessageBox
import platform
import webbrowser
import subprocess

class FfmpegNotInstalledPopup(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("FFmpeg Not Installed")
        self.setStandardButtons(QMessageBox.Cancel)
        self.button(QMessageBox.Cancel).clicked.connect(self.close)
        self.buttonClicked.connect(self.open_ffmpeg_website)

        match (platform.system()):
            case "Windows":
                self.setText("FFmpeg is not installed on your system. Please use Winget to install it.\n\nwinget install --id=Gyan.FFmpeg  -e")
                self.addButton("Install FFmpeg using winget", QMessageBox.ActionRole)
            case "Darwin":
                self.setText("FFmpeg is not installed on your system. Please use Homebrew to install it.\n\nbrew install ffmpeg")
                self.addButton("Install FFmpeg using brew", QMessageBox.ActionRole)
            case "Linux":
                self.setText("FFmpeg is not installed on your system. Please use your package manager to install it.")
                self.addButton("Install FFmpeg using brew", QMessageBox.ActionRole)
            case _:
                self.setText("FFmpeg is not installed on your system. Please install it to continue.")

    def show(self):
        self.exec()
        
    def open_ffmpeg_website(self, button):
        if button.text() == "Cancel":
            print("cancled ffmpeg install")
            return
        match (platform.system()):
            case "Windows":
                subprocess.run(["powershell", "Start-Process", "winget", "-ArgumentList", "'install --id=Gyan.FFmpeg -e'", "-Verb", "RunAs"])
            case "Darwin":
                if subprocess.run(["which", "brew"], capture_output=True).returncode != 0:
                    print("brew not installed")
                    webbrowser.open("https://brew.sh/")
                    popup = isBrewInstalledWindow()
                    popup.show()
                    self.close()
                else:
                    print("brew installed")
                    subprocess.run(["osascript", "-e", 'tell app "Terminal" to do script "brew install ffmpeg"'])
            case "Linux":
                webbrowser.open("https://ffmpeg.org/download.html#build-linux")
            case _:
                webbrowser.open("https://ffmpeg.org/download.html")

class isBrewInstalledWindow(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Homebrew Not Installed")
        self.addButton("I have installed brew on my system", QMessageBox.ActionRole)
        self.buttonClicked.connect(self.installFfmpegUsingBrew)
        self.setText("Homebrew is not installed on your system. Please install it and press the button to continue.")

    def show(self):
        self.exec()
        
    def installFfmpegUsingBrew(self, button):
        subprocess.run(["osascript","-e", 'tell app "Terminal" to do script "brew install ffmpeg"'])
