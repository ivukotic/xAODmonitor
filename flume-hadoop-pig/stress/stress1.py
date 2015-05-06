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
    event['headers']['timestamp']="434324343"
    event['headers']['host']="random_host.example.com"
           
    result={}
    result['cputime']=random.randint(0,1000)
    result['walltime']=random.randint(0,3000)
    result['files']=[]
    result['branches']={}
    
    
    for i in range(random.randint(1,3)):
        result['files'].append("asdf.root")

    for i in range(random.randint(1,10)):
        result['branches']["branch_number_"+str(i)]=random.randint(0,1000)
    
    
    event['body']=result
    events.append(event)
    
    jdata=simplejson.JSONEncoder().encode(events)
    print simplejson.dumps(jdata)
    try:
        data = urllib.urlencode(jdata)
        req = urllib2.Request('http://hadoop-dev.mwt2.org:18080/', data)
        r = urllib2.urlopen(req)
    except urllib2.HTTPError, err:
        print err
    

    if (not w%10):
        et=time.time()
        print w,'insertion rate:',str(w/(et-st)),'Hz'
