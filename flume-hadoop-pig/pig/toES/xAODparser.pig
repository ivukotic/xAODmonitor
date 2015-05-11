REGISTER xAODparser-*.jar
REGISTER json.jar

RECS = LOAD 'xAODcollector.json/xAODdata.2015-05-11/'  using PigStorage as (Rec:chararray);
--dump RECS;

B = FOREACH RECS GENERATE xAODparser.Parser(Rec);
dump B;
