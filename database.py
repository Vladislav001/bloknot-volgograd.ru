import pymongo

class Database:
    client = pymongo.MongoClient("mongodb+srv://admin:123456v@cluster0-4rowy.mongodb.net/test?retryWrites=true&w=majority")
    db = client["parser"]
    collection = db["news"]

    def addRecord(self, data):
        self.collection.insert_one(data)