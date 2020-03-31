from pymongo import MongoClient

class Database:
    client = MongoClient("mongodb+srv://admin:123456v@cluster0-4rowy.mongodb.net/test?retryWrites=true&w=majority")
    #client = MongoClient('mongodb://localhost:27017/')
    db = client["parser"]
    collection = db["news"]

    def addRecord(self, data):
        self.collection.find_one_and_update({
            "name": data['name'],
            "date": data['date'],
            "href": data['href']
        },
            {
                "$set": data
            },
            upsert=True
        )
