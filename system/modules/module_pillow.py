from PIL import Image
from system.modules.module import Module
from global_vars import globals, FinishedType

from system.modules.module_ffmpeg import FFMPEG

class Pillow(Module):
    def __init__(self):
        supportedFormats = (
            "png", "jpg", "jpeg", "bmp", "dds", "dib", "pcx", "ps", "eps", "gif", "apng", "jp2", "j2k", "jpc", "jpf", "jpx", "j2c", "icns", "ico", "im", "jfif", "jpe", "tif", "tiff", "pbm", "pgm", "ppm", "pnm", "pfm", "bw", "rgb", "rgba", "sgi", "tga", "icb", "vda", "vst", "webp", "psd"
        )
        super().__init__(supportedFormats)

    def convert(self, filepath: str, output: str):
        try:
            img_png = Image.open(filepath)
            img_png.save(output)
            globals.update(finishedType=FinishedType.FINISHED)
        except Exception as e:
            print(f"Error converting {filepath} to {output}: {e}")
            self.fallBackToFfmpeg(filepath, output)
            
    def checkDependencies(self)-> bool:
        return True
    
    def fallBackToFfmpeg(self, filepath: str, output: str):
        print("falling back to ffmpeg")
        ffmpeg = FFMPEG()
        ffmpeg.convert(filepath, output)