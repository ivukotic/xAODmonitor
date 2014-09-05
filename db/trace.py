#!/usr/bin/env python
import sys,hashlib, time, urllib2, socket

from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId

try: import simplejson as json
except ImportError: import json

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__

class Path:
    def __init__(self, h, s, d, r):
        self.hash=h
        self.source=s
        self.destination=d
        self.measurements=1
        self.totRate=r
        self.nodes=[]
    def addMeasurement(self, r):
        self.totRate+=r
        self.measurements+=1
    def getAvgRate(self):
        return self.totRate/self.measurements
    def prnt(self):
        print "source:",self.source,"\tdestination:",self.destination,"\tmeasurements:",self.measurements,"\tavg. Rate:",self.getAvgRate(),"\nnodes:",self.nodes
        
class Node:
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

# r=res.remove({}) #all
# r=res.remove({ 'cputime':{'$lt':100} })
# print 'results removed:',r['n']

print 'rows:', res.count()
#print 'data size:', res.dataSize()

print '====================== first 2 rows'
c=res.find().limit(2)
for r in c: 
    print(r)


print '======================== adding hashes manually'
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

print '======================== distinct paths'
distinctPhashes=res.distinct("phash")
print 'distinct hashes:',len(distinctPhashes)
        
        
print '====================== distinct ips'
paths={}
a=time.time()
c=res.find({ "phash":{"$exists":True} })
for r in c:
    ph=r['phash']
    if ph in paths.keys(): 
        paths[ph].addMeasurement(r["rate"])
    else:
        np=Path(ph,r['from'],r['to'],r['rate'])
        for no in r['hops']:
            np.nodes.append(no[0])
        paths[ph]=np    

print "distinct paths:",len(paths)

nodes={}
for p in paths.values():
    for n in p.nodes:
        if n not in nodes:
            nodes[n]=Node(n)
            
print "distinct IPs:  ",len(nodes)
print "paths and ips found in: ",time.time()-a, "seconds"

print '====================== filling IPs '
for p in paths.values():
    c=0
    for n in p.nodes:
        if c>0: nodes[n].addUpstream(p.nodes[c-1])
        if c<(len(p.nodes)-2): nodes[n].addDownstream(p.nodes[c+1])
        nodes[n].counts+=1
        c+=1

for n in nodes.values():
    try:
        req = urllib2.Request("http://geoip.mwt2.org:4288/json/"+n.getIP(), None)
        opener = urllib2.build_opener()
        f = opener.open(req,timeout=5)
        res=json.load(f)
        # print res
        n.longitude=res['longitude']
        n.latitude=res['latitude']
        n.countrycode=res['country_code']
        n.city=res['city']
    except:
        print "# Can't determine client coordinates using geoip.mwt2.org ", sys.exc_info()[0]

for n in nodes.values():    
    try:
        n.name=socket.gethostbyaddr(n.getIP())[0]
    except socket.herror as e:
        print "# Can't determine client name", e
    
    
print '====================== storing nodes into mongo '
    
dbnodes = db['nodes']
dbnodes.remove({})
   
for n in nodes.values():
    n.prnt()
    njs=json.dumps(n, default=jdefault)
    dbnodes.insert(json.loads(njs))

    
print '====================== storing paths into mongo '
dbpaths = db['paths']
dbpaths.remove({})
   
for p in paths.values():
    p.prnt()
    pjs=json.dumps(p, default=jdefault)
    dbpaths.insert(json.loads(pjs))
