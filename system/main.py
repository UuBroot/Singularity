import os
from enum import Enum

import threading

from global_vars import globals, FinishedType

from system.permissionChecker import checkPermissionForFile, givePermissionToFile, givePermissionToFolder, checkPermissionForFolder

### Pillow ###
from system.modules.module_pillow import Pillow
module_pillow = Pillow()
### FFMPEG ###
from system.modules.module_ffmpeg import FFMPEG
moduel_ffmpeg = FFMPEG()
### Text ###
from system.modules.module_text import Text
module_text = Text()

class Modules(Enum):
    PILLOW = "pillow"
    FFMPEG = "ffmpeg"
    TEXT = "text"
    
def convert(pathToFile:str, pathToOutput:str, type = None):
    ##Check permissions
    if not checkPermissionForFile(pathToFile):
        try:
            givePermissionToFile(pathToFile, convert, pathToFile, pathToOutput, type)
        except:
            print("no permission to read file")
            globals.update(finishedType=FinishedType.NOPERMISSION)
        return
        
    if not checkPermissionForFolder(pathToOutput):
        try:
            givePermissionToFolder(pathToOutput, convert, pathToFile, pathToOutput, type)
        except:
            print("no permission to write file")
            globals.update(finishedType=FinishedType.NOPERMISSION)
        return
    
    formatOfFile = getFileType(pathToFile).lower()
    formatToConvertTo = getFileType(pathToOutput).lower()
    
    moduleForFile = getModules(formatOfFile)
    moduleForConversion = getModules(formatToConvertTo)
    moduleToUse = None
    
    if type != None:
        print("force "+type)
        match(type):
            case "ffmpeg":
                moduleForFile = Modules.FFMPEG
                moduleForConversion = Modules.FFMPEG
            case "pillow":
                moduleForFile = Modules.PILLOW
                moduleForConversion = Modules.PILLOW
            case "text":
                moduleForFile = Modules.TEXT
                moduleForConversion = Modules.TEXT
            case _:
                print("module does not exist")
                globals.update(finishedType=FinishedType.WRONGCOMBINATION)
    
    pathToOutput_parts = pathToOutput.split("/") # Split the path into an array and remove the last element
    pathToOutputWithoutFile = "/".join(pathToOutput_parts[:-1])
    if os.path.isfile(pathToFile) and os.path.isdir(pathToOutputWithoutFile):##checks if the input file exists and the output files directory exists
        print(formatOfFile,":",moduleForFile,"  ",formatToConvertTo,":",moduleForConversion)
        ##Error handling for modules
        if moduleForFile == None and moduleForConversion == None:
            print("input and output format is not supported")
            globals.update(finishedType=FinishedType.FILENOTSUPPORTED)
        elif moduleForFile == "" or moduleForFile == None:
            print("input file has unsupported format")
            globals.update(finishedType=FinishedType.FILENOTSUPPORTED)
            return
        elif moduleForConversion == "" or moduleForConversion == None:
            print("output format is not supported")
            globals.update(finishedType=FinishedType.FILENOTSUPPORTED)
            return

        ##Finds the module right to use
        if moduleForFile == moduleForConversion:
            moduleToUse = moduleForFile
        else:
            allModulesforFile = getAllModulesToUse(formatOfFile)
            allModulesforConversion = getAllModulesToUse(formatToConvertTo)
            
            if allModulesforFile.count(moduleForConversion) > 0:
                moduleToUse = moduleForConversion
            elif allModulesforConversion.count(moduleForFile) > 0:
                moduleToUse = moduleForFile
        
        print("using module "+str(moduleToUse).split('.')[1]+" ...")
                
        thread: threading.Thread
        
        match(moduleToUse):
            case Modules.FFMPEG:
                if not moduel_ffmpeg.checkDependencies():
                    print("ffmpeg not installed")
                    globals.update(finishedType=FinishedType.MODULENOTFOUNDERROR)
                    globals.update(errorInModule="ffmpeg")
                    return
                thread = threading.Thread(target=moduel_ffmpeg.convert(pathToFile, pathToOutput))
            case Modules.PILLOW:
                if not moduel_ffmpeg.checkDependencies():
                    print("error finding error module")
                    globals.update(finishedType=FinishedType.MODULENOTFOUNDERROR)
                    globals.update(errorInModule="pillow")
                    return
                thread = threading.Thread(target=module_pillow.convert(pathToFile, pathToOutput))
            case Modules.TEXT:
                if not moduel_ffmpeg.checkDependencies():
                    print("error finding text module")
                    globals.update(finishedType=FinishedType.MODULENOTFOUNDERROR)
                    globals.update(errorInModule="text")
                    return
                thread = threading.Thread(target=module_text.convert(pathToFile, pathToOutput))
            case _:
                print("novalid")

        thread.start()
        thread.join()
        
        if globals.get("finishedType") == FinishedType.FINISHED:
            print("saved to "+str(pathToOutput))
        else:
            print("the file was not saved :/")
        
    else:
        print("""
              not a valid file \n
              pathToFile: """+pathToFile+""" \n
              pathToOutput: """+pathToOutput+"""
              
              """)
        
        globals.update(finishedType=FinishedType.NOTAVALIDFILE)
    
def getFileType(path):
    return os.path.splitext(os.path.basename(path))[1][1:]

def getModules(format):
    if moduel_ffmpeg.formatSupported(format):
        return Modules.FFMPEG
    elif module_pillow.formatSupported(format):
        return Modules.PILLOW
    elif module_text.formatSupported(format):
        return Modules.TEXT
    
def getAllModulesToUse(format) -> list:
    modules = []
    if module_pillow.formatSupported(format):
        modules.append(Modules.PILLOW)
    if moduel_ffmpeg.formatSupported(format):
        modules.append(Modules.FFMPEG)
    if module_text.formatSupported(format):
        modules.append(Modules.TEXT)
    return modules