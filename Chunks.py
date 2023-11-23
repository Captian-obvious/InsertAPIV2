import base64,basicTypes,Buffer,errorHandler,LZ4,os,pyrbxm,sys,requests,robloxapi
def createTable(length,val):
    arr=[]
    for i in range(length):
        arr.append(val)
    ##end
    return arr
##end
def conditionalSet(condition,val1,val2):
    if ((condition)==True):
        return val1
    else:
        return val2
    ##endif
##end
def VirtualInstance(classID, className, ref):
    class vi:
        ClassId=classID
        ClassName=className
        Ref=ref
        Properties={}
        Children=[]
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
        rbxm.InstanceRefs[ref-1]=VirtualInstance(ClassID, ClassName, ref)
    ##end
##end
def META(chunk, rbxm):
    buffer=chunk.Data
    for i in range(buffer.readNumber("<I4")):
        k=basicTypes.String(buffer)
        v=basicTypes.String(buffer)
        rbxm.Metadata[k]=v
    ##end
##end
def PRNT(chunk, rbxm):
    buffer=chunk.Data
    ver=buffer.read()
    if (ver!="\0"):
        chunk.Error("Invalid PRNT version")
    ##endif
    count=buffer.readNumber("<I4")
    child_refs=basicTypes.RefArray(buffer, count)
    parent_refs=basicTypes.RefArray(buffer, count)
    for i in range(count):
        childID=child_refs[i-1]
        parentID=parent_refs[i-1]
        child=rbxm.InstanceRefs[childID]
        parent=conditionalSet(parentID>=0,rbxm.InstanceRefs[parentID],None)
        if (not child):
            chunk.Error(f"Could not parent {str(childID)} to {str(parentID)} because child {str(childID)} was nil")
        ##end
        if (parentID>=0 and not parent):
            chunk.Error(f"Could not parent {childID} to {str(parentID)} because parent {str(parentID)} was nil")
        ##end
        parentTable=conditionalSet(parent!=None,parent.Children,rbxm.Tree)
        parentTable.append(child)
    ##end
##end
def PROP(chunk, rbxm):
    buffer=chunk.Data
    classID=buffer.readNumber("<I4")
    classref=rbxm.ClassRefs[classID-1]
    refs=classref.Refs
    sizeof=classref.Sizeof
    name=basicTypes.String(buffer)
    optTypeIdCheck=ord(buffer.read(1, False)) == 0x1E
    if (optTypeIdCheck):
        buffer.seek(1)
    ##endif
    typeID=ord(buffer.read())
    properties=[]
    if (typeID == 0x01 or typeID == 0x1D):
        for i in range(sizeof):
            properties[i]=basicTypes.String(buffer)
        ##end
    elif (typeID==0x02):
        for i in range(sizeof):
            properties[i]=buffer.read()!="\0"
        ##end
    elif (typeID==0x03):
        properties=basicTypes.Int32Array(buffer, sizeof)
    ##endif
##end
def SSTR(chunk, rbxm):
    buffer=chunk.Data
    ver=buffer.readNumber("<I4")
    if (ver!=0):
        chunk.Error("Invalid SSTR version")
    ##endif
    for i in range(buffer.readNumber("<I4")):
        buffer.read(16)
        rbxm.Strings[i-1]=basicTypes.String(buffer)
    ##end
##end
