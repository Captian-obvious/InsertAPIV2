from api import app
def test():
    pass
##end
def conditionalSet(condition,val1,val2):
    if ((condition)==True):
        return val1
    else:
        return val2
    ##endif
##end
def extract(byte,field,width):
    width=conditionalSet(width!=None,width,1)
    shifted_number=byte >> (width-1)
    mask = (1 << width) - 1
    extracted_bits=shifted_number & mask
    extracted_number=bin(extracted_bits)[2:]
    decimal_value=int(extracted_number, 2)
##end
