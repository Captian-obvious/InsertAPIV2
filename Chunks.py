import base64,basicTypes,Buffer,errorHandler,LZ4,os,pyrbxm,sys,requests,robloxapi

def VirtualInstance(classID, className, ref):
    class vi:
        ClassId=classID
        ClassName=className
        Ref=ref
        Properties={}
        Children={}
    ##end
    return vi
##end

def INST(chunk, rbxm):
    buf=chunk.Data
    ClassID=buf:readNumber("<I4")
    ClassName=BasicTypes.String(buf)
##end
