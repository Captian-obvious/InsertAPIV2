import base64,os,pyrbxm,sys,requests,robloxapi
from pyrxbm.binary import BinaryRobloxFile
from main import app,getRequest
##class COMPILER:
def parse(file):
    parsedString = ""
    with open(file, "rb") as file:
        root = BinaryRobloxFile()
        root.deserialize(file)
        return str(root)
    ##endwith
##end
##end
