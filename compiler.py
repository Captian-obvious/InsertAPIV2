import base64,os,sys,rbxm,requests,robloxapi
from api import app,getRequest
##class COMPILER:
def parse(file):
    parsedString = ""
    f = rbxm.open(file)
    for (object in f.Objects):
        if (isInstance(object)):
            parseInstance(object)
        ##endif
    ##end
##end
##end
