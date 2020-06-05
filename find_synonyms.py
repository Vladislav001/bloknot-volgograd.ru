from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pymystem3 import Mystem
import re

#sys.path.append('../')
from database import Database

# получение фраз из бд
def get_phrases() :
	# Подключение к бд
	db = Database()

	phrases = db.getAllPhrases()
	return phrases

# нормализация токенов
def normalize_tokens(articles) :

	united_articles = []

	text = ' '.join(articles)
	normal_text = Mystem().lemmatize(text.lower())
	
	normal_text = delete_empty_elements(normal_text)

	return normal_text

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

# убирает повторения из списка
def unic_list(data):
	unic_list = []
	for el in data:
		if not el in unic_list:
			unic_list.append(el)
	return unic_list

print("Start finding synonims")

spark = SparkSession\
    .builder\
    .appName("SimpleApplication")\
    .getOrCreate()


# получаем факты
facts = []
phrases = get_phrases()
for phrase in phrases:
	facts.append(phrase['facts']['name'])


# нормализуем факты
# очищаем от лишнего факты и нормализуем
cleared_facts = []
for fact in facts:
	fact_pieces = fact.split(' ')
	cleared_fact_pieces = delete_empty_elements(fact_pieces)
	normalized_facts = normalize_tokens(cleared_fact_pieces)
	cleared_facts.append(' '.join(normalized_facts))

# Составляем список из неповторяющихся фактов
unic_cleared_facts = unic_list(cleared_facts)

# Ищем синонимы к фактам
model = Word2VecModel.load("word2vec")

# достаем слова из словаря
vectors = model.getVectors().collect()
vocabulary = []
for vector in vectors:
	vocabulary.append(vector["word"])

result = {}

# ищем синонимы к словам фактов
for unic_cleared_fact in unic_cleared_facts:
	dict_fact_pieces = {}	

	# разбиваем факт на части (на отдельные слова)
	pieces_of_unic_cleared_fact = unic_cleared_fact.split(" ")

	# для каждой части факта пытаемся найти синоним
	for piece_of_unic_cleared_fact in pieces_of_unic_cleared_fact:

		# если часть факта находится в словаре, то находим ей синоним
		if piece_of_unic_cleared_fact in vocabulary:

			# щем синонимы
			synonyms = model.findSynonyms(piece_of_unic_cleared_fact, 5).collect()

			# найденные синонимы запоминем в dictionary
			dict_synonyms = {}
			for synonym in synonyms:
				dict_synonyms[synonym["word"]] = synonym["similarity"]

			dict_fact_pieces[piece_of_unic_cleared_fact] = dict_synonyms

	result[unic_cleared_fact] = dict_fact_pieces

print(result)




spark.stop()

print("End finding synonims")

