import base64,Buffer,errorHandler,os,pyrbxm,struct,sys,requests,robloxapi
def conditionalSet(condition,val1,val2):
    if ((condition)==True):
        return val1
    else:
        return val2
    ##endif
##end
def listToString(s,sep,i,j):
    str1=""
    for ele in s:
        str1=str1+ele
        if (sep!=None):
            str1=str1+sep
        ##endif
    ##end
    return str1
##end
def lrotate(n,d):
    return (n << d)|(n >> (32 - d))
##end
def rrotate(n,d):
    return (n >> d)|(n << (32 - d)) & 0xFFFFFFFF
##end
def transformInt(x):
    return conditionalSet(x % 2 == 0,x / 2,-(x + 1) / 2)
##end
def rbxF32(x):
    x=rrotate(x, 1)
    return struct.unpack(">f", struct.pack(">I4", x))
##end
def String(buffer):
    return buffer.read(buffer.readNumber("<I4"))
##end
def Int32(buffer):
    return transformInt(buffer.readNumber(">I4"))
##end
def Int64(buffer):
    return transformInt(buffer.readNumber(">I8"))
##end
def Float32(buffer):
    return rbxF32(buffer.readNumber(">I4"))
##end
def Float64(buffer):
    return buffer.readNumber("<d")
##end
def InterleaveArrayWithSize(buffer, count, sizeof):
    if (count<0):
        return Buffer.new("", False)
    ##endif
    stream=buffer.read(count * sizeof)
    out=createTable(count)
    for i in range(count):
        chunk=createTable(sizeof)
        for s in range(sizeof):
            bitPos=(i-1)+(count*s)
            chunk[s-1]=stream[bitPos:bitPos+1]
        ##end
        out[i-1]=concat(chunk)
    ##end
    return Buffer.new(concat(out),False)
##end
def unsignedIntArray(buffer, count):
    if (count<0):
        return []
    ##endif
    o=createTable(count)
    strings=InterleaveArrayWithSize(buffer, count, 4)
    for i in range(count):
        o[i-1]=strings.readNumber("<I4")
    ##end
    return o
##end
