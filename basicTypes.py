import base64,Buffer,errorHandler,os,pyrbxm,struct,sys,requests,robloxapi
def conditionalSet(condition,val1,val2):
    if ((condition)==True):
        return val1
    else:
        return val2
    ##endif
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
