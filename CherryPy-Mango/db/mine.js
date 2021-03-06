conn = new Mongo();
printjson(db.adminCommand('listDatabases').databases);
db = conn.getDB("xAOD");

print("rows: ", db.testData.find().count())

//print ("====================== first 2 rows")
//db.testData.find().limit(2)

//db.testData.remove({}) #all
//db.testData.remove({ 'cputime':{'$lt':100} })

//while(True):a=db.testData.count();time.sleep(10);print db.testData.count()-a;
//print 'data size:', db.testData.dataSize()
    
print("====================== where cputime <200")
c= db.testData.find({ 'cputime':{'$lt':200} },{'cputime':1,'walltime':1})
print("found:",c.length(),"rows")
print("first row:")
printjson( c[0] );

print ("======================== adding hash manually")
db.testData.find({ "bhash":{"$exists":false} }).forEach(function(r){
    brs=Object.keys(r.branches).join(""); 
    //print(brs); 
    bhash=hex_md5(brs);
    //print(bhash);
    db.testData.update( {'_id':r['_id']}, {"$set":{'bhash':bhash}} )
    })

print("================ make sure there is an index on bhash.");
db.testData.ensureIndex( { "bhash": 1 } )        
        
print("====================== aggregating all.")       
agr=db.testData.aggregate([
                { '$match':{'cputime':{'$lt':2000}} },
                { '$group':{ '_id':"$bhash", 'totalCPU':{'$sum':"$cputime"}, 'totalWALL':{'$sum':"$walltime"} } } ])
                
printjson(agr.result)
        
print("====================== map reduce. on bhash. sums of cputimes.")      
lastrun=1404156881
function bhashmapTimes(){ var val=emit(this.bhash,{c:this.cputime, w:this.walltime}) };
function bhashreduceTimes(key,values){ 
    redVal={c:0,w:0};
    for (var i=0;i<values.length;i++){
        redVal.c+=values[i].c;
        redVal.w+=values[i].w;
        }
    return redVal;
    }
db.testData.mapReduce( bhashmapTimes, bhashreduceTimes,'mr_times', query={'timestamp':{'$gt':lastrun}} )
db.mr_times.find().forEach( function(d){
    print ("bHash:", d._id);
    printjson(d.value);
    })


print("====================== map reduce. on bhash. entries read per branch.")
lastrun=1404156881
que={'timestamp':{'$gt':lastrun}}
sor={'bhash': 1} 

function mapfunction(){ emit(this.bhash,this.branches) };
function reducefunction(key,Branches){
    reducedBranches = Branches[0];
    for (var b in Branches[idx]){
        for (var idx = 1; idx < Branches.length; idx++) {
            reducedBranches[b] += Branches[idx][b];
        }
    }
    return reducedBranches;
}

r=db.testData.mapReduce( mapfunction, reducefunction,'mr_branch_usage', query=que, sort=sor)
printjson(r)
db.mr_branch_usage.find().forEach( function(d){
    print ("bHash:", d._id); 
    //printjson(d.value); 
    })
