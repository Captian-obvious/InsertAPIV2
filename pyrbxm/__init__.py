import datatypes,tree
import bin as binary
def readBinary(file):
    with open(file, "rb") as file:
        root = binary.BinaryRobloxFile()
        root.deserialize(file)
        return str(root)
    ##endwith
##end
