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
    
    events=[]
    
    event={}
    event['headers']={}
    event['headers']['timestamp']=str(time.time())
    event['headers']['host']="random_host.example.com"
           
    result={}
    result['cputime']=random.randint(0,1000)
    result['walltime']=random.randint(0,3000)
    result['files']=[]
    result['branches']={}
    
    for i in range(random.randint(1,3)):
        result['files'].append("asdf.root")

    for i in range(random.randint(1,4)):
        result['branches']["branch_number_"+str(i)]=random.randint(0,1000)
    
    
    event['body']=simplejson.dumps(result)
    events.append(event)
    
    # print simplejson.dumps(events)
    
    try:
        req = urllib2.Request('http://hadoop-dev.mwt2.org:18080/')
        req.add_header('Content-Type', 'application/json')
        r = urllib2.urlopen(req, simplejson.dumps(events))
    except urllib2.HTTPError, err:
        print err
    

    if (not w%10):
        et=time.time()
        print w,'insertion rate:',str(w/(et-st)),'Hz'
