#!/usr/bin/env python
import requests
import json as simplejson
import random
import time

s = requests.Session()

st=time.time()
rows=10000

for i in range(rows):
    
    result={}
    result['cputime']=random.randint(0,1000)
    result['walltime']=random.randint(0,3000)
    result['files']=[]
    result['branches']={}
    for i in range(random.randint(1,10)):
        result['files'].append("asdf.root")

    for i in range(random.randint(990,998)):
        result['branches']["branch_number_"+str(i)]=random.randint(0,1000)
    
    data=simplejson.JSONEncoder().encode(result)
    
    r = s.post('http://db.mwt2.org:8080/', params={'data': data})
    print r.status_code, r.text

et=time.time()
print 'insertion rate:',str(rows/(et-st)),'Hz'
