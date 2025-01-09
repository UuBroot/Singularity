from enum import Enum

class FinishedType(Enum):
    FINISHED = 0
    CANCELED = 1
    NOTAVALIDFILE = 2
    WRONGCOMBINATION = 3
    FILENOTSUPPORTED = 4
    MODULENOTFOUNDERROR = 5
    
globals = {
    "current_percentage": 0.0,
    "finishedType": FinishedType.CANCELED,
    "errorInModule": ""
}