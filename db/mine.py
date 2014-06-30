#!/usr/bin/env python
from pymongo import MongoClient
import json as simplejson

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
c=res.find({ 'cputime':{'$lt':200} },{'cputime','walltime'})
for r in c: print(r)

print '====================== aggregating all.'        
c=res.aggregate([
                { '$match':{'cputime':{'$lt':2000}} },
                { '$group':{ '_id':"$timestamp", 'totalCPU':{'$sum':"$cputime"}, 'totalWALL':{'$sum':"$walltime"} } } ])
print c

print '====================== map reduce.'      
lastrun=1403800000;  
c=res.mapReduce(
    function(){ emit(this.timestamp,this.cputime); },
    function(key,values){ return Array.sum(values) },
    {
        query:{timestamp:{'$gt':lastrun}},
        out: 'skim'
    }
)
print c
c=db.skim.find()
for r in c: print(r)