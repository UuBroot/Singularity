from global_vars import globals
class Module:
    percentage = 0.0
    convertion_id: int
    def __init__(self, supportedFormats: tuple, convertion_id):
        self.supportedFormats = supportedFormats
        self.convertion_id = convertion_id

    def formatSupported(self, format: str):
        return self.supportedFormats.__contains__(format)

    def convert(self, filepath: str, output: str):
        print("module error")

    def terminate(self):
        return

    def checkDependencies(self)-> bool:
        print("module error")
        return False

    def updatePercentage(self, value):
        current_list = globals.get("percentageList")
        current_list[self.convertion_id] = value
        globals.update(percentageList=current_list)