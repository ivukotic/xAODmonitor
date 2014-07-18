#!/usr/bin/env python
import string
import json as simplejson
import cherrypy
import os,time
import json as simplejson

logfile = open('xAODraw.txt', 'wa')

def replaceLogFile():
    print 'replacing Log File...'
    logfile.close()
    if not os.path.exists( os.getcwd() + "/LogFiles"):
        print 'creating a directory for them.'
        os.makedirs(os.getcwd() + "LogFiles")
    os.rename(os.getcwd() + 'xAODraw.txt',os.getcwd() + '/LogFiles/xAODraw'+str(int(time.time()))+'.txt')
    logfile = open('xAODraw.txt', 'wa')
    
class xAODreceiver(object):
    exposed = True
    @cherrypy.tools.accept(media='application/json')
    def __init__(self):
        self.counter=0
    def POST(self, data):
        ts=int(time.time())
        result=simplejson.JSONDecoder().decode(data)
        result["timestamp"]=ts
        simplejson.dump(result,logfile)
        self.counter+=1
        print self.counter
        if not self.counter%100:
            replaceLogFile()
        return 'OK'
    
    
        
if __name__ == '__main__':    
    cherrypy.config.update({'tools.log_headers.on': False})
    print cherrypy.config
    cherrypy.quickstart(xAODreceiver(), '/', '/home/ec2-user/xAODmonitor/amazon/xAODstore.conf')
    