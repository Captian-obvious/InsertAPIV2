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
    page = """
    <p id='change' class='red3 center ta_c'>Here you will find links to the Reference Documents</p>
    <p class='red3 center'>
        <!--BEGIN DOCUMENTS PAGES-->
        Reference Documents:<br>
        - <a href='/info.asp'>Info</a><br>
        - <a href='/server.py'>Server</a><br>
        - <a href='/terms.asp'>Terms & Conditions</a><br>
        - <a href='/contact.asp'>Contact</a><br>
        <!--END DOCUMENT PAGES-->
    </p>
    """
    theid = None
    myQuery = getParams(str(request.url))
    if (myQuery!=None):
        idq = str(myQuery[0])
        tyq = None
        if (len(myQuery)>1):
            tyq = str(myQuery[1])
        ##endif
        if (idq!=None):
            theid=int(idq.split('=')[1])
            if (theid!=None):
                if (tyq==None or tyq.lower()=='type=model'):
                    page = """
                    <p id='change' class='red3 center ta_c'>AssetId automatically detected. Downloading..</p>
                    <script>
                        setTimeout(function(){
                            document.location.replace('/')
                        },2000)
                    </script>
                    """
                    asset = insertserver.downloadAsset(theid)
                elif (tyq.lower()=='type=audio' or tyq.lower()=='type=sound'):
                    asset = None
                ##endif
            ##endif
        ##endif
    ##endif
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Insert Cloud API - Welcome</title>
        <link rel='icon' href='/images/favicon.ico'/>
        <link rel='stylesheet' href='/css/styles-main.css'/>
    </head>
    <body>
        <div id='page_content' class='center a_up'>
            <h1 class='red1 center'>Welcome!</h1>
            <h2 class='red2 center ta_c'>Welcome to the Insert Cloud landing page!</h2>
            """+page+"""
        </div>
    </body>
</html>
"""
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
            theid=int(idq.split('=')[1])
            if (theid!=None):
                if (tyq==None or tyq.lower()=='model'):
                    asset = insertserver.downloadAsset(theid)
                elif (tyq.lower()=='audio' or tyq.lower()=='sound'):
                    asset = None
                ##endif
            ##endif
        ##endif
    ##endif
    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Insert Cloud API - Asset Downloader</title>
        <link rel='icon' href='/images/favicon.ico'/>
        <link rel='stylesheet' href='/css/styles-main.css'/>
    </head>
    <body>
        <h1 class='red1'>Insert Cloud API Server: </h1>
        <h2 class='red2'>Download Asset Request Recieved.</h2>
        <p class='red3'>Asset Location: <a href='/assets/v1/"""+str(theid)+"""'>/assets/v1/"""+str(theid)+"""</a></p>
    </body>
</html>
"""
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
@app.route('/credits.asp')
def creditsPage():
    return insertserver.credits()
##end
#Static Pages

#Server stuff
def getParams(url):
    if (len(url.split('?'))>1):
        query = url.split('?')[1]
        params = query.split('&')
        return params
    ##endif
##end

class insertserver:
    def downloadAsset(assetid,type='model'):
        if (type=='model'):
            url = 'https://assetdelivery.roblox.com/v1/asset/?id='+str(assetid)
            req = requests.get(url)
            if (req.status_code==200):
                rawData = req.content
                asset = open('api/assets/v1/'+str(assetid),'wb')
                asset.write(bytearray(rawData))
                return asset
            ##endif
        elif (type=='audio'):
            url = 'https://api.hyra.io/audio/'+str(assetid)
            req = requests.get(url)
            if (req.status_code==200):
                rawData = req.content
                asset = open('api/assets/v1/'+str(assetid),'wb')
                asset.write(bytearray(rawData))
                return asset
            ##endif
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
                    <li>@CaptianObvious - Lead Developer</li>
                    <li>@UnknownUser (terminated) - Deployment Manager</li>
                    <li>Fallen</li>
                </ul><br>
                <u>Maintained By:</u>
                <ul>
                    <li>@Robuyasu</li>
                </ul><br>
                <u>Developed by:</u>
                <ul>
                    <li>@CaptianObvious</li>
                </ul>
                <u>Testing and Standardization</u>
                <ul>
                    <li>Fallen</li>
                </ul>
            </p>
        </div>
    </body>
</html>
"""
    ##end
##end
