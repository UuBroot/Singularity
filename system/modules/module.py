class Module():
    def __init__(self, supportedFormats: tuple):
        self.supportedFormats = supportedFormats
        pass
    
    def formatSupported(self, format: str):
        return self.supportedFormats.__contains__(format)
    
    def convert():
        print("module error")