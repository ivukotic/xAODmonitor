#!/usr/bin/env python
import random
import string
import json as simplejson
import cherrypy
import time
import json as simplejson

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db=client.xAOD
collection = db.testData


class xAODreceiver(object):
    exposed = True
    @cherrypy.tools.accept(media='application/json')
    
    def POST(self, data):
        ts=int(time.time())
        result=simplejson.JSONDecoder().decode(data)
        result["timestamp"]=ts
        collection.insert(result)
        return 'OK'
        
if __name__ == '__main__':    
    cherrypy.config.update({'tools.log_headers.on': False})
    print cherrypy.config
    cherrypy.quickstart(xAODreceiver(), '/', '/home/ivukotic/xAODmonitor/server/xAODstore.conf')
    
