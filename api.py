#Modules & Flask
import base64,os,server,sys,requests,robloxapi
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
def downloaderPage():
    myQuery = getParams(request.url)
    theid=None
    if (myQuery!=None):
        idq = myQuery[0]
        tyq = None
        if (len(myQuery)>1):
            tyq=myQuery[1]
        ##endif
        if (idq!=None):
            theid=int(idq)
            if (theid!=None):
                if (tyq==None or tyq.lower()=='model'):
                    asset = insertserver.downloadAsset(theid)
                elif (tyq.lower()=='audio' or tyq.lower()=='sound'):
                    asset = None
                ##endif
            ##endif
        ##endif
    ##endif
##end
@app.route('/api/parser.py')
def parserPage():
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
#Static Pages

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
    def restart():
        server.restart(request)
    ##end
    def credits():
        return """
<!DOCTYPE html>
<html>
    <head>
        <title>Insert Cloud API - Credits</title>
        <link rel='icon' href='/images/favicon.ico'/>
        <link rel='stylesheet' href='/css/styles-main.css'/>
    </head>
    <body>
        <div id='page-content' class='center va_c'>
            <h1 class='red1 center'>Credits: </h1>
            <p class='red1 center'>
                <u>Management:</u><br>
                <ul>
                    <li>@CaptianObvious - App Manager</li>
                    <li>@Robuyasu - App Contributer</li>
                    <li>Fallen - Testing and Standardization</li>
                </ul><br>
                <u>Maintained By:</u>
                <ul>
                    <li>@Robuyasu</li>
                </ul><br>
                <u>Developed by:</u>
                <ul>
                    <li>@CaptianObvious</li>
                </ul>
            </p>
        </div>
    </body>
</html>
"""
    ##end
##end

