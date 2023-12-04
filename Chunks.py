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
def extract(number, field, width):
    width=conditionalSet(width!=None,width,1)
    mask=(1 << width) - 1
    return (number >> field) & mask
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
def parseBitFlag(byte, bitFlag):
    output=[]
    for i in range(0,7):
        bit=2^i
        if (extract(byte,bit)):
            output.insert(i,bitFlag[bit])
        ##endif
    ##end
    return tuple(output)
##end
def newNumberSequence(count,keypoints):
    virtualNumberSequence={
        'keypointCount':count,
        'keypoints':keypoints,
    }
    return virtualNumberSequence
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
FACES_BIT_FLAG={}
AXES_BIT_FLAG={}
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
    if (typeID==0x01 or typeID==0x1D):
        for i in range(sizeof):
            properties[i-1]=basicTypes.String(buffer)
        ##end
    elif (typeID==0x02):
        for i in range(sizeof):
            properties[i-1]=buffer.read()!="\0"
        ##end
    elif (typeID==0x03):
        properties=basicTypes.Int32Array(buffer, sizeof)
    elif (typeID==0x04):
        properties=basicTypes.RbxF32Array(buffer, sizeof)
    elif (typeID==0x05):
        for i in range(sizeof):
            properties[i-1]=basicTypes.Float64(buffer)
        ##end
    elif (typeID==0x06):
        scale=basicTypes.RbxF32Array(buffer, sizeof)
        offset=basicTypes.Int32Array(buffer, sizeof)
        for i in range(sizeof):
            properties[i-1]={'scale':scale[i],'offset':offset[i]}
        ##end
    elif (typeID==0x07):
        scaleX=basicTypes.RbxF32Array(buffer, sizeof)
        scaleY=basicTypes.RbxF32Array(buffer, sizeof)
        offsetX=basicTypes.Int32Array(buffer, sizeof)
        offsetY=basicTypes.Int32Array(buffer, sizeof)
        for i in range(sizeof):
            properties[i-1]={'scaleX':scaleX[i],'offsetX':offsetX[i],'scaleY':scaleY[i],'offsetY':offsetY[i]}
        ##end
    elif (typeID==0x08):
        for i in range(sizeof):
            properties[i-1]={
                'oX':buffer.readNumber("<f"),
                'oY':buffer.readNumber("<f"),
                'oZ':buffer.readNumber("<f"),
                'dX':buffer.readNumber("<f"),
                'dY':buffer.readNumber("<f"),
                'dZ':buffer.readNumber("<f")
            }
        ##end
    elif (typeID==0x09):
        for i in range(sizeof):
            byte=ord(buffer.read())
            properties[i-1]=parseBitFlag(byte, FACES_BIT_FLAG)
        ##end
    elif (typeID==0x0A):
        for i in range(sizeof):
            byte=ord(buffer.read())
            properties[i-1]=parseBitFlag(byte, AXES_BIT_FLAG)
        ##end
    elif (typeID==0x0B):
        ints=basicTypes.unsignedIntArray(buffer, sizeof)
        for i in range(sizeof):
            properties[i-1]={"value":ints[i]}
        ##end
    elif (typeID==0x0C):
        r=basicTypes.RbxF32Array(buffer, sizeof)
        g=basicTypes.RbxF32Array(buffer, sizeof)
        b=basicTypes.RbxF32Array(buffer, sizeof)
        for i in range(sizeof):
            properties[i-1]={"r":r,"g":g,"b":b}
        ##end
    elif (typeID==0x0D):
        x=basicTypes.RbxF32Array(buffer, sizeof)
        y=basicTypes.RbxF32Array(buffer, sizeof)
        for i in range(sizeof):
            properties[i-1]={"x":x,"y":y}
        ##end
    elif (typeID==0x0E):
        x=basicTypes.RbxF32Array(buffer, sizeof)
        y=basicTypes.RbxF32Array(buffer, sizeof)
        z=basicTypes.RbxF32Array(buffer, sizeof)
        for i in range(sizeof):
            properties[i-1]={"x":x,"y":y,"z":z}
        ##end
    elif (typeID==0x10):
        #CFrame
        matricies=createTable(sizeof)
        for i in range(sizeof):
            rawOrientation=ord(buffer.read())
            if rawOrientation>0:
                orientID = rawOrientation - 1
                R0=orientID // 6
                R1=orientID % 6
                R2=[R0,R1]
                matricies[i]=[R0, R1, R2]
            else:
                r00, r01, r02=buffer.readNumber("<f"), buffer.readNumber("<f"), buffer.readNumber("<f")
                r10, r11, r12=buffer.readNumber("<f"), buffer.readNumber("<f"), buffer.readNumber("<f")
                r20, r21, r22=buffer.readNumber("<f"), buffer.readNumber("<f"), buffer.readNumber("<f")
                matricies[i]=[r00, r10, r20, r01, r11, r21, r02, r12, r22]
            ##endif
        ##end
    elif (typeID==0x11):
        #QUATERNIONS
        quaternions=[]
        for i in range(sizeof):
            quaternions.append({
                'x': buffer.readNumber("<f"),
                'y': buffer.readNumber("<f"),
                'z': buffer.readNumber("<f"),
                'w': buffer.readNumber("<f")
            })
        ##end
        cfX=basicTypes.RbxF32Array(buffer, sizeof)
        cfY=basicTypes.RbxF32Array(buffer, sizeof)
        cfZ=basicTypes.RbxF32Array(buffer, sizeof)
        properties=[]
        for i in range(sizeof):
            q=quaternions[i-1]
            properties.append([cfX[i], cfY[i], cfZ[i], q['x'], q['y'], q['z'], q['w']])
        ##end
    elif (typeID==0x12):
        #Enum
        properties=basicTypes.unsignedIntArray(buffer, sizeof)
    elif (typeID==0x13):
        #Ref
        properties=basicTypes.RefArray(buffer, sizeof)
    elif (typeID==0x14):
        #Vector3int16
        for i in range(sizeof):
            properties[i-1]=[buffer.readNumber("<i2"),buffer.readNumber("<i2"),buffer.readNumber("<i2")]
        ##end
    elif (typeID==0x15):
        #NumberSequence
        for i in range(sizeof):kpCount=buffer.readNumber("<I4")
            kp=createTable(kpCount)
            for c in range(len(kp)):
                kp[c-1]=[buffer.readNumber("<f"),buffer.readNumber("<f"),buffer.readNumber("<f")]
            ##end
            properties[i-1]=newNumberSequence(kpCount,kp)
        ##end
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
