#!/usr/bin/env python
import urllib,urllib2
import json as simplejson
import random
import time

import socket
timeout = 2
socket.setdefaulttimeout(timeout)

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
        req = urllib2.Request('http://db.mwt2.org:8080/', data, {'Content-Type': 'application/json'})
        r = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        print err
    

    if (not w%10):
        et=time.time()
        print w,'insertion rate:',str(w/(et-st)),'Hz'
