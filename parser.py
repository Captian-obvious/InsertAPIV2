import base64,os,pyrbxm,sys,requests,robloxapi
from pyrxbm.binary import BinaryRobloxFile
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
