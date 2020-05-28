from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import Word2Vec
from pyspark.ml.feature import StopWordsRemover

import sys

#sys.path.append('../')
from database import Database


def load_articles_from_db_to_folder() :

	# Подключение к бд
	db = Database()

	print("Loading and saving articles from db")

	# Сохранение статей
	saving_folder_name = "articles"
	articles = db.getAllNews()
	for article in articles:
		output_file_name = saving_folder_name + "/" + str(article["_id"]) + ".txt"
		f = open(output_file_name, 'w')
		f.write(article["text"]);
	print("Articles have been saved")


print("start Wor2vec analyzer")


spark = SparkSession\
    .builder\
    .appName("SimpleApplication")\
    .getOrCreate()

# Загрузка статей с бд в папку /arcticles
load_articles_from_db_to_folder()

# Загрузка всех статей из указанной папки
input_data = spark.sparkContext.wholeTextFiles('articles/*.txt')

# из rdd в датафрейм
prepared = input_data.map(lambda x: ([x[1]]))
df = prepared.toDF()
prepared_df = df.selectExpr('_1 as text')

# Разбиваем на токены
tokenizer = Tokenizer(inputCol='text', outputCol='words')
words = tokenizer.transform(prepared_df)

# Удалияем стоп-слова
stop_words = StopWordsRemover.loadDefaultStopWords('russian')
remover = StopWordsRemover(inputCol='words', outputCol='filtered', stopWords=stop_words)
filtered = remover.transform(words)

# Построить модель Word2Vec
word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol='words', outputCol='result')
model = word2Vec.fit(words)
w2v_df = model.transform(words)
for row in w2v_df.collect():
    #print(row)
    text, words, vector = row
    print("Text: [%s] => \nVector: %s\n" % (", ".join(words), str(vector)))

spark.stop()

print("done Wor2vec analyzer")
