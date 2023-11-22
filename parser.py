import base64,Buffer,LZ4,os,pyrbxm,sys,requests,robloxapi
from pyrbxm.binary import BinaryRobloxFile
from api import app,jsonify,getRequest
HEADER = "<roblox!"
RBXM_SIGNATURE = "\x89\xff\x0d\x0a\x1a\x0a"
ZSTD_HEADER = "\x28\xB5\x2F\xFD"
##class COMPILER:
def parse(file):
    parsedString = ""
    with open(file, "rb") as file:
        root = BinaryRobloxFile()
        root.deserialize(file)
        return str(root)
    ##endwith
##end
def toJson(obj):
    jsonify(obj)
##end
