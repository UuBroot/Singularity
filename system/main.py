import os
from enum import Enum
import sys
import threading

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

    if os.path.isfile(pathToFile):

        # Checks if the input and output files use the same module
        if moduleForFile != moduleForConversion or moduleForFile == None:
            if moduleForFile == "":
                print("input file has unsupported format")
            elif moduleForConversion == "":
                print("output format is not supported")
            else:
                #TODO: Fix out of index crash
                print("wrong combination of file used and format to convert to \n----\nmodule for "+formatOfFile+":"+str(moduleForFile).split('.')[1]+" != module for "+formatToConvertTo+": "+str(moduleForConversion).split('.')[1])
            sys.exit(1)
        
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
    
def getFileType(path):
    return os.path.splitext(os.path.basename(path))[1][1:]

def getModuleToUse(format):
    if module_pillow.formatSupported(format):
        return ModuleToUse.PILLOW
    elif moduel_ffmpeg.formatSupported(format):
        return ModuleToUse.FFMPEG
    elif module_text.formatSupported(format):
        return ModuleToUse.TEXT