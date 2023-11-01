import .binary,.datatypes,.tree
from .binary import BinaryRobloxFile
def readBinary(file):
    with open(file, "rb") as file:
        root = BinaryRobloxFile()
        root.deserialize(file)
        return str(root)
    ##endwith
##end
