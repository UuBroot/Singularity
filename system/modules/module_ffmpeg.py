from system.modules.module import Module
import ffmpeg
import subprocess
import sys

class FFMPEG(Module):
    def __init__(self):
        supportedFormats = (
            "mp4", "webm", "flac", "apng", "asf", "ea","mp3","wav", "mov","a64","aac","ac3","adts","adx","afc","aiff","apm", "aptx","ast", "au","avi","avif","binka","bit","caf","dds_pipe","dfpwm","dvd","eac3","f4v","fits","flv","g722","genh","gif","h264","hevc", "ircam","ismv","ivf","latm","loas","m4v","mjpeg","moflex","m4a","mp2","mp3","mpeg","mtv","mulaw","mxf","nut","obu","oga","ogg","ogv","opus","psp","sbc","sox","spdif","spx","svs","tta","vag","vob","voc","w64","wav","webm","webp", "wtv", "wv"
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
                .output(output)
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