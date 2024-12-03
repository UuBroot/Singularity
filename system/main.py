import os
from enum import Enum
from system.modules.module_pillow import convert as convImg
import filetype

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
    match(format):
        case "png":
            return ModuleToUse.PILLOW
        case "jpg":
            return ModuleToUse.PILLOW
        case "jpeg":
            return ModuleToUse.PILLOW