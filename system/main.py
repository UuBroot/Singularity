import os
from enum import Enum
import sys
import threading

from global_vars import globals, FinishedType

### Pillow ###
from system.modules.module_pillow import Pillow
module_pillow = Pillow()
### FFMPEG ###
from system.modules.module_ffmpeg import FFMPEG
moduel_ffmpeg = FFMPEG()
### Text ###
from system.modules.module_text import Text
module_text = Text()

class ModuleToUse(Enum):
    PILLOW = "pillow"
    FFMPEG = "ffmpeg"
    TEXT = "text"
    
def convert(pathToFile:str, pathToOutput:str, type = None):    
    formatOfFile = getFileType(pathToFile)
    formatToConvertTo = getFileType(pathToOutput)
    
    moduleForFile = getModuleToUse(formatOfFile)
    moduleForConversion = getModuleToUse(formatToConvertTo)
    
    if type != None:
        print("force "+type)
        match(type):
            case "ffmpeg":
                moduleForFile = ModuleToUse.FFMPEG
                moduleForConversion = ModuleToUse.FFMPEG
            case "pillow":
                moduleForFile = ModuleToUse.PILLOW
                moduleForConversion = ModuleToUse.PILLOW
            case "text":
                moduleForFile = ModuleToUse.TEXT
                moduleForConversion = ModuleToUse.TEXT
            case _:
                print("module does not exist")
                globals.update(finishedType=FinishedType.WRONGCOMBINATION)

    pathToOutput_parts = pathToOutput.split("/") # Split the path into an array and remove the last element
    pathToOutputWithoutFile = "/".join(pathToOutput_parts[:-1])
    if os.path.isfile(pathToFile) and os.path.isdir(pathToOutputWithoutFile):
        
        # Checks if the input and output files use the same module
        if moduleForFile != moduleForConversion or moduleForFile == None:
            if moduleForFile == "":
                print("input file has unsupported format")
            elif moduleForConversion == "":
                print("output format is not supported")
            else:
                print("wrong combination of file used and format to convert to")
                globals.update(finishedType=FinishedType.WRONGCOMBINATION)
            return
        
        print("using module "+str(moduleForFile).split('.')[1]+" ...")
        
        thread: threading.Thread
        
        match(moduleForFile):
            case ModuleToUse.FFMPEG:
                thread = threading.Thread(target=moduel_ffmpeg.convert(pathToFile, pathToOutput))
            case ModuleToUse.PILLOW: #pillow as fallback for ffmpeg for images
                thread = threading.Thread(target=module_pillow.convert(pathToFile, pathToOutput))
            case ModuleToUse.TEXT:
                thread = threading.Thread(target=module_text.convert(pathToFile, pathToOutput))
            case _:
                print("novalid")
        thread.start()
        thread.join()
        print("saved to "+str(pathToOutput))
        
    else:
        print("not a valid file")
        globals.update(finishedType=FinishedType.NOTAVALIDFILE)
    
def getFileType(path):
    return os.path.splitext(os.path.basename(path))[1][1:]

def getModuleToUse(format):
    if module_pillow.formatSupported(format):
        return ModuleToUse.PILLOW
    elif moduel_ffmpeg.formatSupported(format):
        return ModuleToUse.FFMPEG
    elif module_text.formatSupported(format):
        return ModuleToUse.TEXT