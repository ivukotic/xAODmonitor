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

print '======================== distinct paths'
distinctPhashes=res.distinct("phash")
print 'distinct hashes:',len(distinctPhashes)
        
        
print '====================== distinct ips'
distinctPaths={}
distinctIPs={}
a=time.time()
c=res.find({ "phash":{"$exists":True} })
for r in c:
    ph=r['phash']
    if ph in distinctPaths.keys(): continue 
    distinctPaths[ph]=[]
    for ip in r['hops']:
        distinctPaths[ph].append(ip[0])
        if ip[1] not in distinctIPs.keys():
            distinctIPs[ip[0]] = IP(ip[0])

print "distinct paths:",len(distinctPaths)
print "distinct IPs:  ",len(distinctIPs)
print "paths and ips found in: ",time.time()-a, "seconds"

print '====================== filling IPs '
for path in distinctPaths.values():
    pl=len(path)
    for h in range(pl):
        ip=distinctIPs[path[h]]
        if h>0: ip.addUpstream(path[h-1])
        if h<(pl-2): ip.addDownstream(path[h+1])
        ip.counts+=1

for ip in distinctIPs.values():
    try:
        req = urllib2.Request("http://geoip.mwt2.org:4288/json/"+ip.getIP(), None)
        opener = urllib2.build_opener()
        f = opener.open(req,timeout=5)
        res=json.load(f)
        # print res
        ip.longitude=res['longitude']
        ip.latitude=res['latitude']
        ip.countrycode=res['country_code']
        ip.city=res['city']
    except:
        print "# Can't determine client coordinates using geoip.mwt2.org ", sys.exc_info()[0]

for ip in distinctIPs.values():    
    try:
        ip.name=socket.gethostbyaddr(ip.getIP())[0]
    except socket.herror as e:
        print "# Can't determine client name", e
    
nodes = db['nodes']
       
for ip in distinctIPs.values():
    ip.prnt()
    njs=json.dumps(ip, default=jdefault))
    nodes.insert(json.loads(njs))

