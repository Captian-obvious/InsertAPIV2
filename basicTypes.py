import Buffer

def String(buffer):
    return buffer.read(buffer.readNumber("<I4"))
##end
