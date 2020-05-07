##################################
## надо разгрести вместе с файлами сайтика
##################################
from pymongo import MongoClient

class Database:
    client = MongoClient("mongodb+srv://admin:123456v@cluster0-4rowy.mongodb.net/test?retryWrites=true&w=majority")
    #client = MongoClient('mongodb://localhost:27017/')
    db = client["parser"]
    collectionNews = db["news"]
    collectionPhrases = db["phrases"]

    # Добавить/обновить запись в БД (новости)
    def addNews(self, data):
        self.collectionNews.find_one_and_update({
            "name": data['name'],
            "date": data['date'],
            "href": data['href']
        },
            {
                "$set": data
            },
            upsert=True
        )

    # Получить все записи из БД - не рекомендуется использовать при кол-ве > 1000 (новости)
    def getAllNews(self):
        data = self.collectionNews.find({})
        return list(data)

    # Пагинация (новости)
    def getPaginationNews(self, pageNum, pageSize):
        skips = int(pageSize) * (int(pageNum) - 1)
        data = self.collectionNews.find({}).skip(skips).limit(pageSize)
        return list(data)

    # Добавить запись в БД (фразы - предложения с фактами)
    def addPhrase(self, data):
        self.collectionPhrases.insert_one({
            "sentence": data['sentence'],
            "facts": data['facts'],  # [{ 'type': '' 'name': '' }, { 'type': '' 'name': '' }],
            }
        )

     # Получить все записи из БД - не рекомендуется использовать при кол-ве > 1000 (фразы - предложения с фактами)
    def getAllPhrases(self):
        data = self.collectionPhrases.find({})
        return list(data)

    # Пагинация (фразы - предложения с фактами)
    def getPaginationPhrases(self, pageNum, pageSize):
        skips = int(pageSize) * (int(pageNum) - 1)
        data = self.collectionPhrases.find({}).skip(skips).limit(pageSize)
        return list(data)
##################################################################
#
########################################################



import re 

# открытие файла
inputFile = "raw_output.txt"
f = open(inputFile, 'r')
text = f.read();

# находим предложения с фактами
regSentenceWithFact = r".+\n(?:\s*(?:PersonFact|PlaceFact)\n\s*{\n\s*.+\n\s*})+"
textsWithFacts = re.findall(regSentenceWithFact, text);

# очищаем найденные части от табов и переносов строки
sentences = []
for textWithFacts in textsWithFacts:
	sentence = textWithFacts.replace("\n", ""); # удаляем переносы строки
	sentence = sentence.replace("\t", ""); # удаляем табуляцию
	sentences.append(sentence)

# вытаскиваем персон из найденных частей и удаляем их из этих частей
regPerson = r"PersonFact\s*{\s*.+\s*}"
regPlace = r"PlaceFact\s*{\s*.+\s*}"


outs = {}
print("Sending...")
db = Database()
for sentence in sentences:

	out = {}

	person = re.search(regPerson, sentence)
	if person != None:
		# вырезаем найденный факт - оставляя только предложение
		sentence = re.sub(regPerson, "", sentence)
		person_name = person.group().replace("PersonFact{Name = ", "");
		person_name = person_name.replace("}", "");


		out["facts"] = { "type" : "person", "name" : person_name}

	place = re.search(regPlace, sentence)
	if place != None:
		sentence = re.sub(regPlace, "", sentence)
		place_name = place.group().replace("PlaceFact{Name =", "");
		place_name = place_name.replace("}", "");
		out["facts"] = { "type" : "place", "name" : place_name}

	out["sentence"] = sentence
	db.addPhrase(out);
	
print("Sended!")






