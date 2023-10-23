import base64,pyrbxm,os,sys,requests,robloxapi
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
