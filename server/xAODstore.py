#!/usr/bin/env python

# curl -H 'Content-Type: application/json' -d @d.json "http://db.mwt2.org:8080/" 
# curl -H 'Content-Type: application/json' -d @d.json "http://db.mwt2.org:8080/trace"
# cat d.json 
# { "method" : "guru.test", "params" : [ "Guru" ], "id" : 123 }

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

tdb=client.trace
tcollection = tdb.fax
tnodes=tdb.nodes

def jsonp(func):
    def foo(self, *args, **kwargs):
        callback, _ = None, None
        if 'callback' in kwargs and '_' in kwargs:
            callback, _ = kwargs['callback'], kwargs['_']
            del kwargs['callback'], kwargs['_']
        ret = func(self, *args, **kwargs)
        if callback is not None:
            ret = '%s(%s)' % (callback, simplejson.dumps(ret))
        return ret
    return foo   

class IPs(object):
    exposed = True
    @jsonp
    
    def MyMethod(self, arg1):
        print arg1
        # requ=cherrypy.request.json
        # nods=tnodes.find().limit(10)
        return 'Works'    
    
class Trace(object):
    exposed = True
    @cherrypy.tools.json_in()
    
    def POST(self):
        ts=int(time.time())
        result=cherrypy.request.json
        result["timestamp"]=ts
        tcollection.insert(result)
        return 'trace OK.'
        
class xAODreceiver(object):
    exposed = True
    trace=Trace()
    ips=IPs()
    
    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_in()
    
    def POST(self):
        ts=int(time.time())
	data=cherrypy.request.json
        data["timestamp"]=ts
	collection.insert(data)
        return 'OK'
        
if __name__ == '__main__':    
    cherrypy.config.update({'tools.log_headers.on': False})
    print cherrypy.config
    cherrypy.quickstart(xAODreceiver(), '/', '/home/ivukotic/xAODmonitor/server/xAODstore.conf')