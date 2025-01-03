from PIL import Image
from system.modules.module import Module

class Pillow(Module):
    def __init__(self):
        supportedFormats = (
            "png", "jpg", "jpeg", "bmp", "dds", "dib", "pcx", "ps", "eps", "gif", "apng", "jp2", "j2k", "jpc", "jpf", "jpx", "j2c", "icns", "ico", "im", "jfif", "jpe", "tif", "tiff", "pbm", "pgm", "ppm", "pnm", "pfm", "bw", "rgb", "rgba", "sgi", "tga", "icb", "vda", "vst", "webp"
        )
        super().__init__(supportedFormats)

    def convert(self, filepath: str, output: str):
        img_png = Image.open(filepath)
        img_png.save(output)
