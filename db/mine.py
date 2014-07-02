#!/usr/bin/env python
from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
import json as simplejson
import hashlib

client = MongoClient('localhost', 27017)
db=client.xAOD
res = db.testData

# res.remove({}) #all
# res.remove({ 'cputime':{'$lt':100} })

print 'rows:', res.count()
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

print '====================== map reduce.'      
lastrun=1404156881;  
mapfunction = Code("function(){ emit(this.timestamp,this.cputime) };")
reducefunction = Code("function(key,values){ return Array.sum(values) };")
c=res.map_reduce( mapfunction, reducefunction,'skim', query={'timestamp':{'$gt':lastrun}} )
print c
c=db.skim.find()
for r in c: print(r)


print '======================== adding hash manually'
c=res.find({ 'timestamp':{'$gt':1404156881}},{'branches':1}).limit(10000)
for r in c:
    brs=r['branches']
    #print rid, brs
    brnames=''.join(brs.keys())
    #print rid, brnames
    bhash = hashlib.md5(brnames).hexdigest()
    print bhash
    res.update( {'_id':r['_id']}, {"$set":{'qwerty':bhash}} )