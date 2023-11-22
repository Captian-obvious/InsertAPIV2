import base64,errorHandler,os,pyrbxm,struct,sys,requests,robloxapi

def conditionalSet(var,el):
    if (var!=None):
        return var
    else:
        return el
    ##endif
##end

def clamp(n,min,max):
    if (n<min):
        return min
    elif (n>max):
        return max
    else:
        return n
    ##endif
##end

def new(datstr,allowOverflows):
    class Stream:
        Offset=0
        Source=datstr
        Length=len(datstr)
        IsFinished=False
        LastUnreadBytes=0
        AllowOverflows=conditionalSet(allowOverflows,False)
        def read(datlen, shift):
            datlen=conditionalSet(datlen,1)
            shift=conditionalSet(shift,True)
            dat=Stream.Source[Stream.Offset:Stream.Offset+datlen+1]
            dataLength=len(dat)
            unreadBytes=datlen-dataLength
            if (unreadBytes>0 and Stream.AllowOverflows!=True):
                errorHandler.error("Buffer went out of bounds and AllowOverflows is false")
            ##end
            if (shift==True):
                Stream.seek(datlen)
    		##end
            Stream.LastUnreadBytes=unreadBytes
            return dat
        ##end
        def seek(datlen):
            datlen=conditionalSet(datlen,1)
            Stream.Offset=clamp(Stream.Offset+datlen,0,Stream.Length)
            Stream.IsFinished=(Stream.Offset>=Stream.Length)
        ##end
    ##end
    return Stream
##end
