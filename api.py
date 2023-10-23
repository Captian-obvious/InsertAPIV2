#Modules & Flask
import base64,requests,robloxapi
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
@app.route('/compiler.py')
def compilerPage():
    myQuery = getParams(request.url)
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
