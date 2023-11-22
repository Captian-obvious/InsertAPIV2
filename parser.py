import base64,Buffer,Chunks,errorHandler,LZ4,os,pyrbxm,sys,requests,robloxapi
from pyrbxm.binary import BinaryRobloxFile
from api import app,jsonify,getRequest
HEADER = "<roblox!"
RBXM_SIGNATURE = "\x89\xff\x0d\x0a\x1a\x0a"
ZSTD_HEADER = "\x28\xB5\x2F\xFD"
VALID_CHUNK_IDENTIFIERS = {
    "END\0":True,
    "INST":True,
    "META":True,
    "PRNT":True,
    "PROP":True,
    "SIGN":True,
    "SSTR":True
}
CHUNK_MODULES={
    "INST":Chunks.INST,
    "META":Chunks.META,
    "PRNT":Chunks.PRNT,
    "PROP":Chunks.PROP,
    "SSTR":Chunks.SSTR
}
def createTable(length,val):
    arr=[]
    for i in range(length):
        arr.append(val)
    ##end
    return arr
##end
def procChunkType(chunkStore,id,rbxm):
    chunks=chunkStore[id]
    f=CHUNK_MODULES[id]
    if (chunks and f):
        for x in range(len(chunks)):
            chunk=chunks[x]
            if (chunk!=None):
                f(chunk, rbxm)
            ##endif
        ##end
    ##endif
##end
##class COMPILER:
def parse(file):
    parsedString = ""
    with open(file, "rb") as file:
        rbxmBuffer=Buffer.new(file.read(), False)
        # Read metadata / header
        if (rbxmBuffer.read(8)!=HEADER or rbxmBuffer.read(6)!=RBXM_SIGNATURE):
            errorHandler.error("Provided file does not match the header of an RBXM file.")
        ##end
        if (rbxmBuffer.read(2)!="\0\0"):
            errorHandler.error("Invalid RBXM version, if Roblox has released a newer version (unlikely), please let me know.")
        ##end
        classCount=rbxmBuffer.readNumber("<i4")
        instCount=rbxmBuffer.readNumber("<i4")
        classRefIds=createTable(classCount)
        instRefIds=createTable(instCount)
        class rbxm:
            ClassRefs=classRefIds
            InstanceRefs=instRefIds
            Tree=[]
            Metadata=[]
            Strings=[]
        ##end
        chunkInfo={}
        for k in VALID_CHUNK_IDENTIFIERS:
            chunkInfo[k]=[]
        ##end
    ##endwith
##end
def toJson(obj):
    jsonify(obj)
##end
