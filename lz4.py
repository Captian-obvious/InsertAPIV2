import base64,Buffer,errorHandler,os,pyrbxm,struct,sys,requests,robloxapi

def decompress(lz4data):
    inputStream=Buffer.new(lz4data)
    compressedLen=struct.unpack("<I4",inputStream.read(4))
    decompressedLen=struct.unpack("<I4",inputStream.read(4))
    reserved=struct.unpack("<I4",inputStream.read(4))
    if (reserved!=0):
        errorHandler.error('Provided Chunk is not LZ4 data!')
    ##endif
    if (compressedLen==0):
        return inputStream.read(decompressedLen)
    ##endif
    outputStream=Buffer.new("")
    while (outputStream.Length<decompressedLen):
        token=ord(inputStream.read())
        litLen=token >> 4
        matLen=(token & 15) + 4
        if (litLen>=15):
            ifinish=False
            while (ifinish!=True):
                nextByte=ord(inputStream.read())
                litLen=litLen+nextByte
                if (nextByte!=0xFF):
                    ifinish=True
                ##endif
                literal = inputStream.read(litLen)
                outputStream.append(literal)
                outputStream.toEnd()
                if (outputStream.Length<decompressedLen):
                    offset=struct.unpack("<I2",inputStream.read(2))
                ##endif
            ##end
        ##endif
    ##end
##end
