#Modules & Flask
import base64,os,sys,requests,robloxapi
from flask import Flask,jsonify,request
#DEFINE APP
app = Flask(__name__)
#Define Some Functions
def getRequest():
    return request
##end
#Dynamic Pages
@app.route('/')
def index():
    myQuery = getParams(request.url)
##end
@app.route('/api/')
def api():
    myQuery = getParams(request.url)
##end
@app.route('/parser.py')
def compilerPage():
    myQuery = getParams(request.url)
    if (myQuery!=None):
        datq = myQuery[0]
        if (datq!=None):
            s = datq.split('=')
            if (s!=None and len(s)>1):
                data = s[1]
            ##endif
        ##endif
    ##endif
##end

#Server stuff
def getParams(url):
    params = None
    query = url.split('?')[1]
    if (query!=None):
        params = query.split('&')
    ##endif
    return params
##end

class insertserver:
    def downloadAsset(assetid):
        url = 'https://assetdelivery.roblox.com/v1/asset/?id='+assetid
        req = requests.get(url)
        if (req.status_code==200):
            rawData = req.content
            asset = open('api/assets/v1/'+assetid,'wb')
            asset.write(bytearray(rawData))
            return asset
        ##endif
    ##end
##end
