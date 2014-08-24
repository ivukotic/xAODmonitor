#!/usr/bin/env python
import string
import json as simplejson
import cherrypy
import os,time
import json as simplejson

logfile = None
# open('xAODraw.txt', 'w')

def replaceLogFile():
    print 'replacing Log File...'
    if not logfile is None:
        logfile.close()
    logfile = open('/LOGs/xAODraw_'+str(int(time.time()))+'.txt')
    # if not os.path.exists( os.getcwd() + "/LogFiles"):
    #     print 'creating a directory for them.'
    #     try:
    #         os.makedirs(os.getcwd() + "/LogFiles")
    #     except OSError, e:
    #         print ("Error: %s - %s." % (e.filename,e.strerror))
    # try:
    #     os.rename(os.getcwd() + '/xAODraw.txt',os.getcwd() + '/LogFiles/xAODraw_'+str(int(time.time()))+'.txt')
    # except OSError, e:
    #     print ("Error: %s - %s." % (e.filename,e.strerror))
    #
    # logfile = open('xAODraw.txt', 'wa')
    
class xAODreceiver(object):
    exposed = True
    @cherrypy.tools.accept(media='application/json')
    def __init__(self):
        self.counter=0
    def POST(self, data):
        if not self.counter%10:
            if not logfile is None:
                logfile.close()
            logfile = open('/LOGs/xAODraw_'+str(int(time.time()))+'.txt')
        ts=int(time.time())
        result=simplejson.JSONDecoder().decode(data)
        result["timestamp"]=ts
        simplejson.dump(result,logfile)
        self.counter+=1
        print self.counter
        return 'OK'
    
    
        
if __name__ == '__main__':    
    cherrypy.config.update({'tools.log_headers.on': False})
    print cherrypy.config
    cherrypy.quickstart(xAODreceiver(), '/', '/home/ec2-user/xAODmonitor/amazon/xAODstore.conf')
    