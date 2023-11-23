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
    buffer=chunk.Data
    ClassID=buffer.readNumber("<I4")
    ClassName=basicTypes.String(buffer)
    if (buffer.read()=="\1"):
        chunk.Error("Attempt to insert binary model with services")
    ##endif
    count=buffer.readNumber("<I4")
    refs=basicTypes.RefArray(buffer, count)
    class theclass:
        Name=ClassName
        Sizeof=count
        Refs=refs
    ##end
    rbxm.ClassRefs[ClassID]=theclass
    for ref in refs:
        rbxm.InstanceRefs[ref]=VirtualInstance(ClassID, ClassName, ref)
    ##end
##end
