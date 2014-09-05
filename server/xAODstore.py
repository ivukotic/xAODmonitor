#!/usr/bin/env python

# curl -H 'Content-Type: application/json' -d @d.json "http://db.mwt2.org:8080/" 
# curl -H 'Content-Type: application/json' -d @d.json "http://db.mwt2.org:8080/trace"
# cat d.json 
# { "method" : "guru.test", "params" : [ "Guru" ], "id" : 123 }
# curl -H "Accept: application/json" -X post "http://db.mwt2.org:8080/ips"

import random
import string
import cherrypy
import time
import json as simplejson

from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient('localhost', 27017)
db=client.xAOD
collection = db.testData

tdb=client.trace
tcollection = tdb.fax
tnodes=tdb.nodes

class IPs(object):
    exposed = True
    @cherrypy.tools.json_out()
 
    def POST(self):
        # requ=cherrypy.request.json
        nods=tnodes.find()
        ret=[]
        #for n in nods:
	#    d=dumps(n)
        #    ret.append(d)
	for n in nods:
	     upstream=[]
	     downstream=[]
             if n.has_key("upstream"): 
	         up=n["upstream"]
	     else:
                 up=[]
	     for i in up:  upstream.append([int(i),up[i]])
	     if n.has_key("downstream"):
	         down=n["downstream"]
             else:
                 down=[]
	     for i in down:  downstream.append([int(i),down[i]])
             lo=n["longitude"]
	     la=n["latitude"]
             ret.append({ "ip":n["ip"], "name":n["name"], "long":lo, "lat":la, "up":upstream, "down":downstream })
        return ret    
    
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
