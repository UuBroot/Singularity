from enum import Enum

class FinishedType(Enum):
    FINISHED = 0
    CANCELED = 1
    NOTAVALIDFILE = 2
    WRONGCOMBINATION = 3
    FILENOTSUPPORTED = 4
    MODULENOTFOUNDERROR = 5
    NOPERMISSION = 6
    FILECORRUPT = 7
    
globals = {
    "finishedType": FinishedType.CANCELED,
    "errorInModule": "",
    "percentageList": {},
    "convertionInProgress": False,
}