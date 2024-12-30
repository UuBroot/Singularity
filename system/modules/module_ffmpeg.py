from system.modules.module import Module
import ffmpeg
import subprocess
import sys

from global_vars import globals

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
        
        ##Runs the command
        try:
            totalFrames = self.get_total_frames(filepath)
            print(f"Total frames: {totalFrames}")
            process=(
                ffmpeg.input(filepath)
                .output(output)
                .global_args('-progress', '-', '-nostats','-y','-threads','0')
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )
            while process.poll() is None:
                if process.stdout:
                    line = process.stdout.readline()
                    accLine = str(line).split("'")[1].split("\\")[0]
                    if accLine.startswith("frame="):
                        currFrame = int(accLine.split("=")[1])
                        prc = (currFrame/totalFrames)*100
                        globals.update(current_percentage=prc)
                else:
                    break
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
        
    def get_total_frames(self, filepath: str) -> int:
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=nb_read_frames", "-of", "default=nokey=1:noprint_wrappers=1", filepath],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"ffprobe error: {result.stderr}")
            return int(result.stdout.strip())
        except Exception as e:
            print(f"Error getting total frames: {e}")
            return 0