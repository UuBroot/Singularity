class Module():
    percentage = 0.0
    def __init__(self, supportedFormats: tuple):
        self.supportedFormats = supportedFormats
        pass

    def formatSupported(self, format: str):
        return self.supportedFormats.__contains__(format)

    def convert(self, filepath: str, output: str):
        print("module error")

    def terminate(self):
        return

    def checkDependencies(self)-> bool:
        print("module error")
        return False