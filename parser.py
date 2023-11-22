import base64,os,pyrbxm,sys,requests,robloxapi
from pyrbxm.binary import BinaryRobloxFile
HEADER = "<roblox!"
RBXM_SIGNATURE = "\x89\xff\x0d\x0a\x1a\x0a"
ZSTD_HEADER = "\x28\xB5\x2F\xFD"
from api import app,jsonify,getRequest
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
