import tr as tree
import types as datatypes
import bin as binary
def readBinary(file):
    with open(file, "rb") as file:
        root = binary.BinaryRobloxFile()
        root.deserialize(file)
        return str(root)
    ##endwith
##end
