show dbs
use xAOD
show collections

print("rows: ", db.testData.find().count())

print ("====================== first 2 rows")
db.testData.find().limit(2)

//db.testData.remove({}) #all
//db.testData.remove({ 'cputime':{'$lt':100} })

//while(True):a=db.testData.count();time.sleep(10);print db.testData.count()-a;
//print 'data size:', db.testData.dataSize()
    
print("====================== where cputime <200")
c= db.testData.find({ 'cputime':{'$lt':200} },{'cputime':1,'walltime':1})
print("found:",c.length(),"rows")
print("first row:")
c[1]

print("====================== aggregating all.")       
db.testData.aggregate([
                { '$match':{'cputime':{'$lt':2000}} },
                { '$group':{ '_id':"$timestamp", 'totalCPU':{'$sum':"$cputime"}, 'totalWALL':{'$sum':"$walltime"} } } ])


print("====================== map reduce. on time.")      
lastrun=1404156881;  
function mapfunction(){ emit(this.timestamp,this.cputime) };
function reducefunction(key,values){ return Array.sum(values) };
db.testData.mapReduce( mapfunction, reducefunction,'skim', query={'timestamp':{'$gt':lastrun}} )
db.skim.find().forEach( function(d){print ("timestamp:", d._id, "CPUtime:",d.value) } )

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
        
        
print("====================== map reduce. on bhash. sums of cputimes.")      
lastrun=1404156881
function mapfunction(){ emit(this.bhash,this.cputime) };
function reducefunction(key,values){ return Array.sum(values) };
db.testData.mapReduce( mapfunction, reducefunction,'skimOnBhash', query={'timestamp':{'$gt':lastrun}} )
db.skimOnBhash.find().forEach( function(d){print ("bHash:", d._id, "CPUtime:",d.value) } )


print("====================== map reduce. on bhash. entries read per branch.")
lastrun=1404156881
que={'timestamp':{'$gt':lastrun}}
sor={'bhash': 1} 

function mapfunction(){ emit(this.bhash,this.branches) };
function reducefunction(key,Branches){
    reducedBranches = Branches[0];
    for (var idx = 1; idx < Branches.length; idx++) {
        for (var b in Branches[idx]){
            reducedBranches[b] += Branches[idx][b];
        }
    }
    return reducedBranches;
}

db.testData.mapReduce( mapfunction, reducefunction,'skim', query=que, sort=sor)
db.skim.find()
