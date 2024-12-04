import os
from enum import Enum

### Pillow ###
from system.modules.module_pillow import Pillow
module_pillow = Pillow()
### FFMPEG ###
from system.modules.module_ffmpeg import FFMPEG
moduel_ffmpeg = FFMPEG()

class ModuleToUse(Enum):
    PILLOW = "pillow"
    FFMPEG = "ffmpeg"
    
def convert(pathToFile, pathToOutput):
    
    formatToConvertTo = str(pathToOutput).split("/")[-1].split(".")[-1]

    if os.path.isfile(pathToFile):

        # Checks if the input and output files use the same module
        if getModuleToUse(getFileType(pathToFile)) != getModuleToUse(formatToConvertTo) or getModuleToUse(getFileType(pathToFile)) == None:
            if getModuleToUse(getFileType(pathToFile)) == "":
                print("input file has unsupported format")
            elif getModuleToUse(formatToConvertTo) == "":
                print("output format is not supported")
            else:
                print("wrong combination of file used and format to convert to || module for file:"+str(getModuleToUse(getFileType(pathToFile))).split('.')[1]+" != module for conversion: "+str(getModuleToUse(formatToConvertTo)))
            return
        
        print("using module "+str(getModuleToUse(getFileType(pathToFile))).split('.')[1]+" ...")
        
        match(getModuleToUse(getFileType(pathToFile))):
            case ModuleToUse.PILLOW:
                if codec != "":
                    print("codec conversion not supported")
                module_pillow.convert(pathToFile, pathToOutput)
            case ModuleToUse.FFMPEG:
                moduel_ffmpeg.convert(pathToFile, pathToOutput)
            case _:
                print("novalid")
        
        print("saved to "+str(pathToOutput))
        
    else:
        print("not a valid file")
    
def getFileType(path):
    return os.path.splitext(os.path.basename(path))[1][1:]

def getModuleToUse(format):
    if module_pillow.formatSupported(format):
        return ModuleToUse.PILLOW
    elif moduel_ffmpeg.formatSupported(format):
        return ModuleToUse.FFMPEG