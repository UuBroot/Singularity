from system.modules.module import Module
import ffmpeg
import subprocess
import sys

class FFMPEG(Module):
    def __init__(self):
        supportedFormats = (
            "flac",
            "mp4", "webm"
        )
        super().__init__(supportedFormats)

    def convert(self, filepath: str, output: str):
                
        ##Checks if ffmpeg is installed
        if not self.isFfmpegInstalled():
            print("no ffmpeg installed")
            sys.exit(1)
        
        ##Runns the command
        try:
            (
                ffmpeg.input(filepath)
                .output(output, loglevel="quiet")
                .run()
            )
        except Exception as e:
            print(e)
            sys.exit(1)
        
    def isFfmpegInstalled(self):
        try:
            result = subprocess.run(["ffmpeg","-version"], capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            return False
