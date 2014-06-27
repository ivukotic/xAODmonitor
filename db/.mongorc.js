function addResult(result){
	var col = db.testData.results;
	result.timestamp=Math.round((new Date().getTime())/1000);
	col.insert(result);
}

function generateData(branches,num) {
  for (i = 0; i < num; i++) {
   d={};
   for (b = 0; b< branches; b++){
    	d["BranchName_"+b]= Math.round(Math.random()*1000);
    }
    cpt=Math.random()*1000;
    wat=Math.random()*3000;
    r={files:["a.root","b.root"],branches:d,cputime:cpt,walltime:wat}
    addResult(r);
  }
  print(db.testData.results.count());
}

function badEff(){
	db.testData.results.find({ cputime:{$lt:10.0} });
}

function reduceRecent(){
        print(db.testData.results.count());
        print(db.testData.results.dataSize());
	db.testData.results.aggregate([
		{ $match:{cputime:{$lt:200}} },
		{ $group:{ _id:"$timestamp", total:{$sum:"$cputime"} } }
	]);
}
