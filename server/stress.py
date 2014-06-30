#!/usr/bin/env python
import requests
import json as simplejson
import random

s = requests.Session()

for i in range(100):
    
    result={}
    result['cputime']=random.randint(0,1000)
    result['walltime']=random.randint(0,3000)
    result['files']=[]
    result['branches']={}
    for i in range(random.randint(1,10)):
        result['files'].append("asdf.root")

    for i in range(15):
        result['branches']["branch_number_"+str(i)]=random.randint(0,1000)
    
    data=simplejson.JSONEncoder().encode(result)
    
    r = s.post('http://127.0.0.1:8080/', params={'data': data})
    print r.status_code, r.text

