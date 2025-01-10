import os

def checkPermissionForFile(path)->bool:
    if os.access(path, os.R_OK):
        return True
    else:
        return False

def checkPermissionForFolder(path)->bool:
    folderPath = filePathToFolder(path)
    
    if os.access(folderPath, os.R_OK):
        return True
    else:
        return False

def givePermissionToFile(path, function, *args):
    currentPermission = os.stat(path).st_mode

    os.chmod(path, 0o777)
    function(*args)
    os.chmod(path, currentPermission)

    return True

def givePermissionToFolder(path, function, *args):
    folderPath = filePathToFolder(path)
    
    currentPermission = os.stat(folderPath).st_mode

    os.chmod(folderPath, 0o777)
    function(*args)
    os.chmod(folderPath, currentPermission)

    return True

def filePathToFolder(path)->str:
    path_parts = path.split("/")
    pathWithoutFile = "/".join(path_parts[:-1])
    return pathWithoutFile