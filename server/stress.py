#!/usr/bin/env python
import requests
import json as simplejson
import random
import time

s = requests.Session()
headers = {'Content-type': 'application/json'}

st=time.time()
rows=10000

for w in range(rows):
    
    result={}
    result['cputime']=random.randint(0,1000)
    result['walltime']=random.randint(0,3000)
    result['files']=[]
    result['branches']={}
    for i in range(random.randint(1,10)):
        result['files'].append("asdf.root")

    for i in range(random.randint(990,998)):
        result['branches']["branch_number_"+str(i)]=random.randint(0,1000)
    
    data=simplejson.dumps(result)
    try:
        r = s.post('http://db.mwt2.org:8080/', data, headers=headers, timeout=2.0)
        if (r.status_code!=200): print r.status_code, r.text
    except requests.exceptions.HTTPError, err:
        print err
    except requests.exceptions.Timeout, e:
        print "Error: ",e 
    

    if (not w%5):
        et=time.time()
        print w,'insertion rate:',str(w/(et-st)),'Hz'
