import os
from enum import Enum
from system.modules.imagemagicModule import convert as convImgMag
import filetype

class ModuleToUse(Enum):
    IMGMAG = "imagemagic"
    FFMPEG = "ffmpeg"
    
def convert(format, filepath):
    
    if os.path.isfile(filepath):
        
        match(getModuleToUse(getFileType(filepath))):
            case ModuleToUse.IMGMAG:
                convImgMag(filepath, format)
            case _:
                print("novalid")
    else:
        print("not a valid file")
    
def getFileType(path):
    return os.path.splitext(os.path.basename(path))[1][1:]


def getModuleToUse(format):
    match(format):
        case "png":
            return ModuleToUse.IMGMAG
        case "jpg":
            return ModuleToUse.IMGMAG
        case "jpeg":
            return ModuleToUse.IMGMAG