from system.modules.module import Module
import subprocess
import sys
import platform

from global_vars import globals, FinishedType

class FFMPEG(Module):
    convertion_id: int
    def __init__(self, convertion_id):
        supportedFormats = (
            "mp4", "webm", "flac", "apng", "asf", "ea","mp3","wav", "mov","a64","aac","ac3","adts","adx","afc","aiff","apm", "aptx","ast", "au","avi","avif","binka","bit","caf","dds_pipe","dfpwm","dvd","eac3","f4v","fits","flv","g722","genh","gif","h264","hevc", "ircam","ismv","ivf","latm","loas","m4v","mjpeg","moflex","m4a","mp2","mp3","mpeg","mtv","mulaw","mxf","nut","obu","oga","ogg","ogv","opus","psp","sbc","sox","spdif","spx","svs","tta","vag","vob","voc","w64","wav","webm","webp", "wtv", "wv"
        )
        super().__init__(supportedFormats, convertion_id)
        self.convertion_id = convertion_id

    def checkDependencies(self)-> bool:
        return self.isFfmpegInstalled()

    def terminate(self):
        if platform.system() in ["Linux", "Darwin"]:
            subprocess.run("killall ffmpeg", shell=True, check=True, capture_output=True)

    def convert(self, filepath: str, output: str):
        ##Checks if ffmpeg is installed
        if not self.isFfmpegInstalled():
            print("no ffmpeg installed")
            sys.exit(1)
        
        ##Runs the command
        try:
            totalFrames = self.get_total_frames(filepath)
            process = subprocess.Popen(
                ["ffmpeg", "-i", filepath, output, "-progress", "-", "-nostats", "-y", "-threads", "0"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(self.convertion_id)
            print("Started ffmpeg")

            while process.poll() is None:
                if totalFrames == 0:
                    pass
                if process.stdout:
                    line = process.stdout.readline()
                    accLine = line.strip()
                    if accLine.startswith("frame="):
                        currFrame = int(accLine.split("=")[1])
                        prc = (currFrame / totalFrames) * 100
                        try:
                            self.updatePercentage(prc)
                        except Exception as e:
                            print(e)
                        print(globals.get("percentageList"))
        except Exception as e:
            print(e)
            sys.exit(1)

        self.updatePercentage(100.0)
        globals.update(finishedType=FinishedType.FINISHED)

    def isFfmpegInstalled(self):
        try:
            result = subprocess.run(["ffmpeg","-version"], capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            return False
        
    def get_total_frames(self, filepath: str) -> int:
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", filepath],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"ffprobe error: {result.stderr}")
            output = result.stdout.strip()
            if not output.isdigit():
                return 0
            return int(output)
        except Exception as e:
            print(f"Error getting total frames: {e}")
            return 0