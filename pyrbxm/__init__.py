from .binary import *
from .datatypes import *
from .tree import *
def readBinary(file):
    with open(file, "rb") as file:
        root = binary.BinaryRobloxFile()
        root.deserialize(file)
        return str(root)
    ##endwith
##end
