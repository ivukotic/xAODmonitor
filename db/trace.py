#!/usr/bin/env python
from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import json as simplejson
import hashlib, time


class IP:
    def __init__(self,ip):
        self.ip=ip
        self.counts=0
        self.upstream=[]
        self.downstream=[]
        self.name=""
        self.longitude=0
        self.latitude=0
    def getIP(self):
        o1 = int(self.ip / 16777216) % 256
        o2 = int(self.ip / 65536) % 256
        o3 = int(self.ip / 256) % 256
        o4 = int(self.ip) % 256
        return '%(o1)s.%(o2)s.%(o3)s.%(o4)s' % locals()
    def prnt(self):
        print "name:      ",self.name, "\tIP:",self.getIP(), "\tlat/lon: ",self.longitude, self.latitude
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
        if h>0: ip.upstream.append(path[h-1])
        if h<(pl-2): ip.downstream.append(path[h+1])
        ip.counts+=1

for ip in distinctIPs.values():
    ip.prnt()
    

