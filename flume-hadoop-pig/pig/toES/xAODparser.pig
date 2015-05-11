REGISTER xAODparser-*.jar
REGISTER json.jar

RECS = LOAD 'xAODcollector.json/xAODdata.2015-05-11/'  using PigStorage as (Rec:chararray);
--dump RECS;

B = FOREACH RECS GENERATE xAODparser.Parser(Rec) as tuple(fns:chararray,brs:chararray,cnts:chararray);
describe B;
dump B;

C = foreach B generate FLATTEN($0);
dump C;
describe C;