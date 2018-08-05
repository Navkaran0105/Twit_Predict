from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col
import numpy
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression

from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler

from pyspark.ml.evaluation import BinaryClassificationEvaluator,MulticlassClassificationEvaluator

#from pyspark.ml import PipelineModel

sc =SparkContext()
sqlContext = SQLContext(sc)
data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('analysis.csv')
test = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('labelled_test.csv')

data.show(5)
test.show(10)
data.printSchema()

data.groupBy("Sentiment") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()


print("Training Dataset Count: " + str(data.count()))
print("Test Data Count: " + str(test.count()))

# regular expression tokenizer
regexTokenizer = RegexTokenizer(inputCol="SentimentText", outputCol="words", pattern="\\W")

# stop words
add_stopwords = ["http","https","amp","rt","t","c","the","@", "@foxnewspolitics", "#cdnpoli", "@ABC", "@ABCPolitics"]
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

# convert string labels to indexes
label_stringIdx = StringIndexer(inputCol = "Sentiment", outputCol = "label", handleInvalid='keep')

lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
#lrModel = lr.fit(trainingData)


# build the pipeline
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx, lr])

# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(data)
predictions = pipelineFit.transform(test)


predictions.filter(predictions['prediction'] == 0) \
    .select("Sentiment","SentimentText","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

predictions.filter(predictions['prediction'] == 1) \
    .select("Sentiment","SentimentText","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

# Evaluate, metricName=[accuracy | f1]default f1 measure
evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction",labelCol="label")
print("F1: %g" % (evaluator.evaluate(predictions)))

# save the trained model for future use
pipelineFit.save("lregression.model")

# PipelineModel.load("logreg.model")

