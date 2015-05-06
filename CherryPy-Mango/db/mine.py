#!/usr/bin/env python
from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import json as simplejson
import hashlib, time

client = MongoClient('localhost', 27017)
db=client.xAOD
res = db.testData

# r=res.remove({}) #all
# r=res.remove({ 'cputime':{'$lt':100} })
# print 'results removed:',r['n']

print 'rows:', res.count()
#while(True):a=res.count();time.sleep(10);print res.count()-a;
#print 'data size:', res.dataSize()

print '====================== first 2 rows'
c=res.find().limit(2)
for r in c: print(r)
    
print '====================== where cputime <200'
c=res.find({ 'cputime':{'$lt':200} },{'cputime':1,'walltime':1})
for r in c: print(r)

print '====================== aggregating all.'        
c=res.aggregate([
                { '$match':{'cputime':{'$lt':2000}} },
                { '$group':{ '_id':"$timestamp", 'totalCPU':{'$sum':"$cputime"}, 'totalWALL':{'$sum':"$walltime"} } } ])
print c

print '====================== map reduce. on time.'      
lastrun=1404156881;  
mapfunction = Code("function(){ emit(this.timestamp,this.cputime) };")
reducefunction = Code("function(key,values){ return Array.sum(values) };")
c=res.map_reduce( mapfunction, reducefunction,'skim', query={'timestamp':{'$gt':lastrun}} )
print c
c=db.skim.find()
for r in c: print(r)


print '======================== adding hash manually'
a=time.time()
c=res.find({ "bhash":{"$exists":False} })
for r in c:
    brs=r['branches']
    #print rid, brs
    brnames=''.join(brs.keys())
    #print rid, brnames
    bhash = hashlib.md5(brnames).hexdigest()
    #print bhash
    co=res.update( {'_id':r['_id']}, {"$set":{'bhash':bhash}} )
    if (co['ok']!=1.0):
        print 'problem in adding the bhash', co
        break

print "hashes added in: ",time.time()-a, "seconds"
        

print '================ make sure there is an index on bhash.'
#res.ensureIndex( { "bhash": 1 } )        
        
        
print '====================== map reduce. on bhash. sums of cputimes.'      
lastrun=1404156881
mapfunction = Code("function(){ emit(this.bhash,this.cputime) };")
reducefunction = Code("function(key,values){ return Array.sum(values) };")
c=res.map_reduce( mapfunction, reducefunction,'skim', query={'timestamp':{'$gt':lastrun}} )
print c
c=db.skim.find()
for r in c: print(r)


print '====================== map reduce. on bhash. entries read per branch.'      
a=time.time()
lastrun=1404156881
que={'timestamp':{'$gt':lastrun}}
sor={'bhash': 1} 

rf="""
function(key,Branches){ 
    reducedBranches = Branches[0];
    for (var idx = 1; idx < Branches.length; idx++) {
        for (var b in Branches[idx]){
            reducedBranches[b] += Branches[idx][b];
        }
    }
    return reducedBranches;
};
"""

mapfunction = Code("function(){ emit(this.bhash,this.branches) };")
reducefunction = Code(rf);
c=res.map_reduce( mapfunction, reducefunction,'skim', query=que, sort=sor)


print "branches reduced in: ",time.time()-a, "seconds"
print c
c=db.skim.find()
for r in c: print(r)