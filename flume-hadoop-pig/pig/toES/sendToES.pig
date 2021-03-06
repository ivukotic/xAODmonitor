
-- try again the JsonLoader ( see if it can load from directory named with .json )


REGISTER '/usr/lib/pig/piggybank.jar' ;
--REGISTER '/usr/lib/pig/lib/jackson-*.jar';
--REGISTER '/usr/lib/pig/lib/json-*.jar';
--REGISTER '/usr/lib/pig/lib/jython-*.jar';
--REGISTER '/usr/lib/pig/lib/snappy-*.jar';

REGISTER '/share/home/ivukotic/xAODmonitor/jython*.jar';


REGISTER 'myudfs.py' using jython as myfuncs;

REGISTER '/usr/lib/pig/lib/elasticsearch-hadoop-*.jar';
define EsStorage org.elasticsearch.hadoop.pig.EsStorage('es.nodes=http://uct2-es-head.mwt2.org:9200');

RECS = LOAD 'xAODcollector' using PigStorage as (Rec:chararray);

CNTS = foreach RECS generate myfuncs.ParsedData(Rec);

dump CNTS;
 

grJ = group JOBS by (PANDAID, CLOUD, COMPUTINGSITE, PRODSOURCELABEL);
gJOBS = foreach grJ { generate FLATTEN(group) as (PANDAID,CLOUD,COMPUTINGSITE,PRODSOURCELABEL), myfuncs.BagToBag(JOBS); };



--RECS = LOAD 'tests.json/data.01' using JsonLoader('cputime:int, walltime:int');

REGISTER '/home/ivukotic/xAODmonitor/elephant-bird-hadoop-compat-4.1.jar'
REGISTER '/home/ivukotic/xAODmonitor/elephant-bird-pig-4.1.jar'
RECS = LOAD 'tests/data.13.1431022457749.json' using com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad');
A = foreach RECS generate (int)$0#'cputime' as cputime, (int)$0#'walltime' as walltime, (bag{tuple(chararray)})$0#'files' as files, (map[])$0#'branches' as branches;
describe A;

RECS = LOAD 'tests/data1.json' using JsonLoader('accessedFiles: {(fn:chararray)},accessedContainers:(chararray,int),accessedBranches:(chararray,int)');

RECS = LOAD 'xAODcollector.json/xAODdata.2015-05-11/' using JsonLoader('accessedBranches:{chararray,int}');
RECS = LOAD 'xAODcollector.json/xAODdata.2015-05-11/' using JsonLoader('accessedFiles:chararray,accessedContainers:chararray,accessedBranches:chararray');

--RECS = LOAD 'tests/data.json' using JsonLoader('files: {(fn:chararray)}, branches: (br:chararray, reads:int),cputime:int,walltime:int');
--files: {(fn:chararray)}, branches: (br:chararray, reads:int),
-- times:bag{tuple(state:chararray, time:long)};
L = LIMIT RECS 100; dump L;
STORE L INTO 'xaodtest3/xaodtest_record' USING EsStorage();


-- RECS = LOAD 'tests' USING PigStorage(',') AS (F:int,S:int,T:int,N:chararray);
-- STORE RECS INTO 'xaodtest/xaodtest_record' USING EsStorage();



--REGISTER '/usr/lib/pig/lib/avro-*.jar';