import base64,os,sys,requests,robloxapi
from api import app,jsonify
#APP RESTART HANDLER
@app.route('/api/restart/')
def restart(request):
    if (request!=None):
        return 'Server Restarted!'
    ##endif
##end
