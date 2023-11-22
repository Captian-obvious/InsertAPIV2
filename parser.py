import base64,Buffer,errorHandler,LZ4,os,pyrbxm,sys,requests,robloxapi
from pyrbxm.binary import BinaryRobloxFile
from api import app,jsonify,getRequest
HEADER = "<roblox!"
RBXM_SIGNATURE = "\x89\xff\x0d\x0a\x1a\x0a"
ZSTD_HEADER = "\x28\xB5\x2F\xFD"
##class COMPILER:
def parse(file):
    parsedString = ""
    with open(file, "rb") as file:
        rbxmBuffer=Buffer.new(file.read(), False)
        # Read metadata / header
        if (rbxmBuffer.read(8)!=HEADER or rbxmBuffer.read(6)!=RBXM_SIGNATURE):
            errorHandler.error("Provided file does not match the header of an RBXM file.")
        ##end
    ##endwith
##end
def toJson(obj):
    jsonify(obj)
##end
