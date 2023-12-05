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
def Chunk(buffer, chunkIndex):
    chunk={}
    chunk['InternalID']=chunkIndex
    chunk['Header']=buffer.read(4)
    if (chunk['Header'] not in VALID_CHUNK_IDENTIFIERS):
        raise ValueError(f"Invalid chunk identifier {chunk['Header']} on chunk id {chunkIndex}")
    ##endif
    data=None
    lz4Header=buffer.read(16, False)
    compressed=int.from_bytes(lz4Header[:4], 'little')
    decompressed=int.from_bytes(lz4Header[4:8], 'little')
    reserved=lz4Header[8:12]
    zstd_check=lz4Header[12:16]
    if (reserved!=b'\x00\x00\x00\x00'):
        raise ValueError(f"Invalid chunk header on chunk id {chunkIndex} of identifier {chunk['Header']}")
    ##endif
    if (compressed == 0):
        data = buffer.read(decompressed)
    else:
        if (zstd_check==ZSTD_HEADER):
            raise ValueError(f"Chunk id {chunkIndex} of identifier {chunk['Header']} is a ZSTD compressed chunk and cannot be decompressed")
        ##endif
        data = LZ4.decompress(buffer.read(compressed + 12))
    ##endif
    chunk['Data']=Buffer.new(data, False)
    def error(self, msg):
        raise ValueError(f"[{self['Header']}:{self['InternalID']}]: {msg}")
    ##end
    chunk['Error']=error
    return chunk
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
