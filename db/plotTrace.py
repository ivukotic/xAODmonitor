#!/usr/bin/env python
import sys,hashlib, time, urllib2, socket

import pydot

from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId

try: import simplejson as json
except ImportError: import json

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__
        
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
        getDetails()
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
            ip.name=socket.gethostbyaddr(ip.getIP())[0]
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

        

client = MongoClient('localhost', 27017)
db=client.trace
res = db.fax

print '======================== adding hash manually'
a=time.time()
c=res.find({ "phash":{"$exists":False} })
for r in c:
    hps=r['hops']
    #print r, hps
    ips=[]
    for i in hps:
        ips.append(str(i[0]))
    ipsj=''.join(ips)
    #print r, ipsj
    phash = hashlib.md5(ipsj).hexdigest()
    #print phash
    co=res.update( {'_id':r['_id']}, {"$set":{'phash':phash}} )
    if (co['ok']!=1.0):
        print 'problem in adding the phash', co
        break

print "hashes added in: ",time.time()-a, "seconds"



print '======================== distinct sources'
sources=res.distinct("from")
print 'distinct sources:',len(sources)
print '======================== distinct destinations'
destinations=res.distinct("to")
print 'distinct destinations:',len(destinations)

source="MWT2"
destination="AGLT2"
print res.find({"$and": [ {"from":source} , {"to":destination}, {"phash":{"$exists":True}} ] }).count()
rows=res.find({"$and": [ {"from":source} , {"to":destination}, {"phash":{"$exists":True}} ] })
#for r in rows: print r
# find all IPs
distinctIPs={}
distinctPaths={}
for r in rows:
    ph=r['phash']
    if ph in distinctPaths.keys(): continue 
    distinctPaths[ph]=[]
    for h in r['hops']:
        distinctPaths[ph].append(h[0])
        if h[0] not in distinctIPs.keys():
            distinctIPs[h[0]] = IP(h[0])

for ip in distinctIPs.values():
    ip.prnt()
        
# create a graph
g=pydot.Dot(type='digraph', prog='neato',splines='true', overlap='false', size='20,20')


loColor=gradi.HTMLColorToRGB('FFCC00')
hiColor=gradi.HTMLColorToRGB('FF0000')
#colorgradient=1.0/max(weight.values())

for ip in distinctIPs.values():
    # color=gradi.RGBToHTMLColor(gradi.RGBinterpolate(loColor,hiColor,colorgradient*weight[asin]))
    node=pydot.Node(ip.name+" "+ip.getIP(), shape='circle',style='filled')#, fillcolor=color,  fontsize=8+weight[asin])
    # node.set_URL('http://www.amazon.com/gp/product/'+asin)
    # amazonresult=amazon.AmazonAPI(asin)
    # tooltip=amazon.getelement(amazonresult,'Title')
    # node.set_tooltip(tooltip)
    g.add_node(node)

# add the edges
#for ip in distinctIPs.values():
    #for ip.
    #g.add_edge(pydot.Edge(pair[0],pair[1]))

g.write(source+"_to_"+destination+'.svg',format='svg')
g.write(source+"_to_"+destination+'.jpg',format='jpg')

