import base64,struct

def new(datstr,allowOverflows):
    class Stream:
        Offset=0
        Source=datstr
        Length=len(datstr)
        IsFinished=False
        LastUnreadBytes=0
        AllowOverflows=conditionalSet()
        
    ##end
##end
