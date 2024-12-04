import os
from enum import Enum
import sys
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
    
    formatToConvertTo = getFileType(pathToOutput)
    formatOfFile = getFileType(pathToFile)

    if os.path.isfile(pathToFile):

        # Checks if the input and output files use the same module
        if getModuleToUse(formatOfFile) != getModuleToUse(formatToConvertTo) or getModuleToUse(formatOfFile) == None:
            if getModuleToUse(formatOfFile) == "":
                print("input file has unsupported format")
            elif getModuleToUse(formatToConvertTo) == "":
                print("output format is not supported")
            else:
                print("wrong combination of file used and format to convert to \n----\nmodule for "+formatOfFile+":"+str(getModuleToUse(formatOfFile)).split('.')[1]+" != module for "+formatToConvertTo+": "+str(getModuleToUse(formatToConvertTo)))
            sys.exit(1)
        
        print("using module "+str(getModuleToUse(formatOfFile)).split('.')[1]+" ...")
        
        match(getModuleToUse(formatOfFile)):
            case ModuleToUse.PILLOW:
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