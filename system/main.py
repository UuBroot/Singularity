import os
from enum import Enum
import filetype
from system.modules.module_pillow import convert as convImg

#######################
## Supported Formats ##
#######################
### Pillow ###
supportedImageFormats = (
    "png", "jpg", "jpeg", "bmp", "dds", "dib", "pcx", "ps", "eps", "gif", "apng", "jp2", "j2k", "jpc", "jpf", "jpx", "j2c", "icns", "ico", "im", "jfif", "jpe", "tif", "tiff", "pbm", "pgm", "ppm", "pnm", "pfm", "bw", "rgb", "rgba", "sgi", "tga", "icb", "vda", "vst", "webp"
)
### FFMPEG ###
supportedVideoFormats = (
    "mp4"
)

class ModuleToUse(Enum):
    PILLOW = "pillow"
    FFMPEG = "ffmpeg"
    
def convert(format, filepath):
    
    if os.path.isfile(filepath):

        if getModuleToUse(getFileType(filepath)) != getModuleToUse(format):
            print("wrong combination of file used and format to convert to || module for file:"+str(getModuleToUse(getFileType(filepath))).split('.')[1]+" != module for conversion: "+str(getModuleToUse(format)))
            return
        
        print("using module "+str(getModuleToUse(getFileType(filepath))).split('.')[1]+" ...")

        match(getModuleToUse(getFileType(filepath))):
            case ModuleToUse.PILLOW:
                convImg(filepath, format)
            case _:
                print("novalid")
        
        print("saved as export."+format)
        
    else:
        print("not a valid file")
    
def getFileType(path):
    return os.path.splitext(os.path.basename(path))[1][1:]

def getModuleToUse(format):
    if supportedImageFormats.__contains__(format):
        return ModuleToUse.PILLOW
    elif supportedVideoFormats.__contains__(format):
        return ModuleToUse.FFMPEG