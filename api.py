#Modules & Flask
import base64,compiler,os,sys,requests,robloxapi
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
    if (myQuery!=None):
        datq = myQuery[0]
        if (datq!=None):
            
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
