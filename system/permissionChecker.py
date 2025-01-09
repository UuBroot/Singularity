import os

def checkPermissionForFile(path):
    if os.access(path, os.R_OK):
        return True
    else:
        return False