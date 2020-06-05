from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType 
from pyspark.sql.types import ArrayType
from pymystem3 import Mystem
import re
import string
import os



#sys.path.append('../')
from database import Database

spark = SparkSession\
    .builder\
    .appName("SimpleApplication")\
    .getOrCreate()

# нормализация токенов
def normalize_tokens(articles) :

	united_articles = []

	text = ' '.join(articles)
	normal_text = Mystem().lemmatize(text.lower())
	
	normal_text = delete_empty_elements(normal_text)

	return normal_text
	
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
		f.close()
	print("Articles have been saved")			

# удаляет пустые элементы из списка
def delete_empty_elements(data):
	cleared_data = []
	for word in data:
		cleared_word = re.sub('[^А-Яа-я]', '', word.strip())
		cleared_data.append(cleared_word)

	while '' in cleared_data:
		cleared_data.remove('')
	while ' ' in cleared_data:
		cleared_data.remove(' ')

	return cleared_data


# Удаление пунктуации из текста
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

# Удаление разрыва строк из текста
def remove_linebreaks(text):
	text = text.strip()
	text = text.replace('\n', '')
	return text

print("Start finding synonims")

load_articles_from_db_to_folder()

# Загрузка всех статей из указанной папки
input_data = spark.sparkContext.wholeTextFiles('articles/*.txt')

# из rdd в датафрейм
prepared = input_data.map(lambda x: ([x[1]])) \
    .map(lambda x: (remove_linebreaks(x[0]), '1')) \
    .map(lambda x: (remove_punctuation(x[0]), '1'))
df = prepared.toDF()
prepared_df = df.selectExpr('_1 as text')

# Разбиваем на токены
tokenizer = Tokenizer(inputCol='text', outputCol='words')
words = tokenizer.transform(prepared_df)

# Удалияем стоп-слова
stop_words = StopWordsRemover.loadDefaultStopWords('russian')
remover = StopWordsRemover(inputCol='words', outputCol='filtered', stopWords=stop_words)
filtered = remover.transform(words)

clear = udf(lambda x: delete_empty_elements(x), ArrayType(StringType()))
cleared = filtered.withColumn('cleared', clear('filtered'))

normalize = udf(lambda x: normalize_tokens(x), ArrayType(StringType()))
normalized = cleared.withColumn('normalized', normalize('cleared'))

# Построить модель Word2Vec
word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol='normalized', outputCol='result')

model = word2Vec.fit(normalized)

w2v_df = model.transform(normalized)

model.save("word2vec")

'''
for row in w2v_df.collect():
    result = row
    print("Text: [%s] => \nVector: %s\n" % (result[0], result[4]))
'''

spark.stop()


print("Done building model")
