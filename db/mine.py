#!/usr/bin/env python
from pymongo import MongoClient
import json as simplejson

client = MongoClient('localhost', 27017)
db=client.xAOD
res = db.testData

print 'rows:', res.count()
#print 'data size:', res.dataSize()

c=res.find().limit(2)
for r in c:
    print(r)