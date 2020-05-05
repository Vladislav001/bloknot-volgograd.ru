from pymongo import MongoClient

class Database:
    client = MongoClient("mongodb+srv://admin:123456v@cluster0-4rowy.mongodb.net/test?retryWrites=true&w=majority")
    #client = MongoClient('mongodb://localhost:27017/')
    db = client["parser"]
    collectionNews = db["news"]

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