import sys
import re 

sys.path.append('../')
from database import Database

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






