import os
from enum import Enum

import threading

from global_vars import globals, FinishedType

from system.permissionChecker import checkPermissionForFile, givePermissionToFile, givePermissionToFolder, checkPermissionForFolder

### Pillow ###
from system.modules.module_pillow import Pillow

### FFMPEG ###
from system.modules.module_ffmpeg import FFMPEG

### Text ###
from system.modules.module_text import Text

class Modules(Enum):
    PILLOW = "pillow"
    FFMPEG = "ffmpeg"
    TEXT = "text"

class Main:
    convertion_id: int
    module_text: Text
    module_ffmpeg: FFMPEG
    module_pillow: Pillow

    def __init__(self, convertion_id = 0):
        self.convertion_id = convertion_id
        self.module_text = Text(convertion_id)
        self.module_ffmpeg = FFMPEG(convertion_id)
        self.module_pillow = Pillow(convertion_id)

        #adds the default percentage to the percentage entry of the convertion
        current_list = globals.get("percentageList")
        current_list[self.convertion_id] = 0.0
        globals.update(percentageList=current_list)

    def convert(self, pathToFile:str, pathToOutput:str, type = None):
        ##Check permissions
        if not checkPermissionForFile(pathToFile):
            try:
                givePermissionToFile(pathToFile, self.convert, pathToFile, pathToOutput, type)
            except:
                print("no permission to read file")
                globals.update(finishedType=FinishedType.NOPERMISSION)
            return

        if not checkPermissionForFolder(pathToOutput):
            try:
                givePermissionToFolder(pathToOutput, self.convert, pathToFile, pathToOutput, type)
            except:
                print("no permission to write file")
                globals.update(finishedType=FinishedType.NOPERMISSION)
            return

        formatOfFile = self.getFileType(pathToFile).lower()
        formatToConvertTo = self.getFileType(pathToOutput).lower()

        moduleForFile = self.getModules(formatOfFile)
        moduleForConversion = self.getModules(formatToConvertTo)
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
                    return

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
                allModulesforFile = self.getAllModulesToUse(formatOfFile)
                allModulesforConversion = self.getAllModulesToUse(formatToConvertTo)

                if allModulesforFile.count(moduleForConversion) > 0:
                    moduleToUse = moduleForConversion
                elif allModulesforConversion.count(moduleForFile) > 0:
                    moduleToUse = moduleForFile

            print("using module "+str(moduleToUse).split('.')[1]+" ...")

            thread: threading.Thread

            match(moduleToUse):
                case Modules.FFMPEG:
                    if not self.module_ffmpeg.checkDependencies():
                        print("ffmpeg not installed")
                        globals.update(finishedType=FinishedType.MODULENOTFOUNDERROR)
                        globals.update(errorInModule="ffmpeg")
                        return
                    thread = threading.Thread(target=self.module_ffmpeg.convert(pathToFile, pathToOutput))
                case Modules.PILLOW:
                    if not self.module_ffmpeg.checkDependencies():
                        print("error finding error module")
                        globals.update(finishedType=FinishedType.MODULENOTFOUNDERROR)
                        globals.update(errorInModule="pillow")
                        return
                    thread = threading.Thread(target=self.module_pillow.convert(pathToFile, pathToOutput))
                case Modules.TEXT:
                    if not self.module_ffmpeg.checkDependencies():
                        print("error finding text module")
                        globals.update(finishedType=FinishedType.MODULENOTFOUNDERROR)
                        globals.update(errorInModule="text")
                        return
                    thread = threading.Thread(target=self.module_text.convert(pathToFile, pathToOutput))
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

    def getFileType(self, path):
        return os.path.splitext(os.path.basename(path))[1][1:]

    def getModules(self,format):
        if self.module_ffmpeg.formatSupported(format):
            return Modules.FFMPEG
        elif self.module_pillow.formatSupported(format):
            return Modules.PILLOW
        elif self.module_text.formatSupported(format):
            return Modules.TEXT

    def getAllModulesToUse(self, format) -> list:
        modules = []
        if self.module_pillow.formatSupported(format):
            modules.append(Modules.PILLOW)
        if self.module_ffmpeg.formatSupported(format):
            modules.append(Modules.FFMPEG)
        if self.module_text.formatSupported(format):
            modules.append(Modules.TEXT)
        return modules

    def terminate(self):
        self.module_pillow.terminate()
        self.module_ffmpeg.terminate()
        self.module_text.terminate()