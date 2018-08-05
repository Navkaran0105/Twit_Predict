from pyspark.sql.functions import col
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from collections import namedtuple
from pyspark.ml import PipelineModel
from collections import namedtuple
from pyspark.ml import Pipeline
#from pyspark.streaming import Seconds
# from pyspark.sql.functions import desc

#sc = SparkContext("local[2]", "Streaming App")
sc = SparkContext.getOrCreate()
ssc = StreamingContext(sc, 1)
sqlContext = SQLContext(sc)
#ssc.checkpoint( "file:/home/ubuntu/tweets/checkpoint/")

socket_stream = ssc.socketTextStream("127.0.0.1", 5555) # Internal ip of  the tweepy streamer

lines = socket_stream.window(20)
fields = ("SentimentText")
Tweet = namedtuple( 'Tweet', fields )

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def do_something(time, rdd):
    print("========= %s =========" % str(time))
    try:
        Model = PipelineModel.load('lregression.model')
        # Get the singleton instance of SparkSession 
        spark = getSparkSessionInstance(rdd.context.getConf())
        # Convert RDD[String] to RDD[Tweet] to DataFrame
        rowRdd = rdd.map(lambda w: Tweet(w))
        linesDataFrame = spark.createDataFrame(rowRdd)
#        Model = PipelineModel.load('lregression.model')
        cap_stream = Model.transform(linesDataFrame)
        cap_stream.createOrReplaceTempView("tweets")
        lineCountsDataFrame = spark.sql("select SentimentText, prediction from tweets")
        lineCountsDataFrame.show()
        lineCountsDataFrame.coalesce(1).write.format("com.databricks.spark.csv").save(path='Conservative_tweets', format='csv', mode='append', sep='\t')
    except Exception as e:
        print(e.message)
        pass


lines.foreachRDD(do_something)

ssc.start()
ssc.awaitTerminationOrTimeout(300)
