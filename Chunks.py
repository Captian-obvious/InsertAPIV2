import base64,Buffer,errorHandler,LZ4,os,pyrbxm,sys,requests,robloxapi

def VirtualInstance(classID, className, ref):
    class vi:
        ClassId=classID
        ClassName=className
        Ref=ref
        Properties={}
        Children={}
    ##end
    return vi
##end

def INST(chunk, rbxm):
    buf=chunk.Data
##end
