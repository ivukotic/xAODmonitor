REGISTER xAODparser-*.jar
REGISTER json.jar
RECS = LOAD 'xAODcollector.json/xAODdata.2015-05-11/'  using PigStorage as (Rec:chararray);;
B = FOREACH RECS GENERATE xAODparser.Parser(Rec);
dump RECS;
dump B;
