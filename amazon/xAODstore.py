#!/usr/bin/env python
import string
import json as simplejson
import cherrypy
import time
import json as simplejson

class xAODreceiver(object):
    exposed = True
    @cherrypy.tools.accept(media='application/json')
    def __init__(self):
        logfile = open('xAODraw.txt', 'wb')
        self.counter=0
    def POST(self, data):
        ts=int(time.time())
        result=simplejson.JSONDecoder().decode(data)
        result["timestamp"]=ts
        logfile.write(result)
        self.counter+=1
        if self.counter>100:
            logfile.close
        return 'OK'
        
if __name__ == '__main__':    
    cherrypy.config.update({'tools.log_headers.on': False})
    print cherrypy.config
    cherrypy.quickstart(xAODreceiver(), '/', '/home/ec2-user/xAODmonitor/amazon/xAODstore.conf')
    
