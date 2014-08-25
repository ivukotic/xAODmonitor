#!/usr/bin/env python
from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import json as simplejson
import hashlib, time

def Int2IP(ipnum):
    o1 = int(ipnum / 16777216) % 256
    o2 = int(ipnum / 65536) % 256
    o3 = int(ipnum / 256) % 256
    o4 = int(ipnum) % 256
    return '%(o1)s.%(o2)s.%(o3)s.%(o4)s' % locals()


client = MongoClient('localhost', 27017)
db=client.trace
res = db.fax

# r=res.remove({}) #all
# r=res.remove({ 'cputime':{'$lt':100} })
# print 'results removed:',r['n']

print 'rows:', res.count()
#while(True):a=res.count();time.sleep(10);print res.count()-a;
#print 'data size:', res.dataSize()

print '====================== first 2 rows'
c=res.find().limit(2)
for r in c: print(r)

#print '====================== where cputime <200'
#c=res.find({ 'cputime':{'$lt':200} },{'cputime':1,'walltime':1})
#for r in c: print(r)

#print '====================== aggregating all.'        
#c=res.aggregate([
#                { '$match':{'cputime':{'$lt':2000}} },
#                { '$group':{ '_id':"$timestamp", 'totalCPU':{'$sum':"$cputime"}, 'totalWALL':{'$sum':"$walltime"} } } ])
#print c

#print '====================== map reduce. on time.'      
#lastrun=1404156881;  
#mapfunction = Code("function(){ emit(this.timestamp,this.cputime) };")
#reducefunction = Code("function(key,values){ return Array.sum(values) };")
#c=res.map_reduce( mapfunction, reducefunction,'skim', query={'timestamp':{'$gt':lastrun}} )
#print c
#c=db.skim.find()
#for r in c: print(r)


print '======================== adding hash manually'
a=time.time()
c=res.find({ "phash":{"$exists":False} })
for r in c:
    hps=r['hops']
    #print r, hps
    ips=[]
    for i in hps:
        ips.append(str(i[1]))
    ipsj=''.join(ips)
    #print r, ipsj
    phash = hashlib.md5(ipsj).hexdigest()
    #print phash
    co=res.update( {'_id':r['_id']}, {"$set":{'phash':phash}} )
    if (co['ok']!=1.0):
        print 'problem in adding the phash', co
        break

print "hashes added in: ",time.time()-a, "seconds"

#print '================ make sure there is an index on bhash.'
#res.ensureIndex( { "phash": 1 } )        


print '======================== distinct paths'
dp=res.distinct("phash")
print 'unique paths:',len(dp)
        
        
print '====================== distinct ips'
tps={}
uips=set()
a=time.time()
c=res.find({ "phash":{"$exists":True} })
for r in c:
    ph=r['phash']
    if ph in tps.keys: continue 
    tps[ph]=[]
    for ip in r.hops:
        tps[ph]=ip[1]
        uips.add(ip[1])

print len(tps)
print len(uips)

#print '====================== map reduce. on bhash. entries read per branch.'      
#a=time.time()
#lastrun=1404156881
#que={'timestamp':{'$gt':lastrun}}
#sor={'bhash': 1} 


