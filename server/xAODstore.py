#!/usr/bin/env python

# curl -H 'Content-Type: application/json' -d @d.json "http://db.mwt2.org:8080/" 
# curl -H 'Content-Type: application/json' -d @d.json "http://db.mwt2.org:8080/trace"
# cat d.json 
# { "method" : "guru.test", "params" : [ "Guru" ], "id" : 123 }
# curl -H "Accept: application/json" -X post "http://db.mwt2.org:8080/ips"
# curl  -H "Accept: application/json" -X post "http://db.mwt2.org:8080/network?source=MWT2&destination=AGLT2"

import random
import sys,hashlib, urllib2, socket
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
tpaths=tdb.paths


class IP:
    def __init__(self,ip):
        self.ip=ip
        self.counts=0
        self.upstream={}
        self.downstream={}
        self.name=""
        self.longitude=0
        self.latitude=0
        self.countrycode=""
        self.city=""
        self.getDetails()
    def getDetails(self):
        try:
            req = urllib2.Request("http://geoip.mwt2.org:4288/json/"+self.getIP(), None)
            opener = urllib2.build_opener()
            f = opener.open(req,timeout=5)
            res=json.load(f)
            # print res
            self.longitude=res['longitude']
            self.latitude=res['latitude']
            self.countrycode=res['country_code']
            self.city=res['city']
        except:
            print "# Can't determine client coordinates using geoip.mwt2.org ", sys.exc_info()[0]
        try:
            self.name=socket.gethostbyaddr(self.getIP())[0]
        except socket.herror as e:
            print "# Can't determine client name", e 
    def addUpstream(self,ip):
        if ip not in self.upstream:
            self.upstream[ip]=1
        else:
            self.upstream[ip]+=1
    def addDownstream(self,ip):
        if ip not in self.downstream:
            self.downstream[ip]=1
        else:
            self.downstream[ip]+=1
    def getIP(self):
        o1 = int(self.ip / 16777216) % 256
        o2 = int(self.ip / 65536) % 256
        o3 = int(self.ip / 256) % 256
        o4 = int(self.ip) % 256
        return '%(o1)s.%(o2)s.%(o3)s.%(o4)s' % locals()
    def prnt(self):
        print "name:      ",self.name, "\tIP:",self.getIP(), "\tlat/lon: ",self.longitude, self.latitude
        print "country:   ",self.countrycode, "\tcity:",self.city
        print "upstream:  ",self.upstream
        print "downstream:",self.downstream
        print "count:     ",self.counts


class Network(object):
    exposed = True
    @cherrypy.tools.json_out()
 
    def POST(self,source, destination):
        rows=tpaths.find({"$and": [ {"source":source} , {"destination":destination} ] });
        ret={}
        ret['nodes']=[]
        ret['edges']=[]
        no=[]
        ed=[]
        for r in rows:
            c=0
            rate=r['totRate']/r['measurements']
            for n in r['nodes']:
                if n not in no:
                    no.append(n)
                if c<(len(r['nodes'])-1):
                    f=n
                    t=r['nodes'][c+1]
                    found=0
                    for a in ed:
                        if (a[0]==f and a[1]==t):
                            if a[2]<rate: a[2]=rate
                            found=1
                            break
                    if found==0:
                        ed.append([n,t,rate, r['measurements']])
                c+=1
        
        for sn in no:
            n=IP(sn)
            ret['nodes'].append({ "ip":n.ip,"sip":n.getIP(),"name":n.name, "up":n.upstream, "down":n.downstream })
        for se in ed:    
            ret['edges'].append({"from":se[0],"to":se[1],"value":se[2],"title":"%0.4f"%se[2]+" MB/s\n"+str(se[3])+"measurements."}); 
        return ret    


class IPs(object):
    exposed = True
    @cherrypy.tools.json_out()
 
    def POST(self):
        # requ=cherrypy.request.json
        nods=tnodes.find()
        ret=[]
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
    network=Network()
    
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
