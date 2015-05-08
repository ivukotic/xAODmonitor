#!/usr/bin/python
import json
from datetime import datetime

@outputSchema("ntuple(nFiles:int,nContainers:int,nBranches:int)")
def ParsedData(record):
    rec = json.loads(record)
    nFiles=len(a['accessedFiles'])
    nContainers=len(a['accessedContainers'])
    nBranches=len(a['accessedBranches'])
    
    return (nFiles,nContainers,nBranches)
